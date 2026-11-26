#!/usr/bin/env python3
"""Builtin tool name census: compare documented tool names against the code.

The code side is the set of tool names Aleph actually registers. The code
itself names that set, so the gate reads the code's own lists instead of
guessing from a regex sweep:

* `BUILTIN_TOOL_DEFINITIONS` (`src/executor/builtin_registry/definitions.rs`) —
  the catalogue the run loop offers the model;
* `REGISTRY_ONLY_DESCRIPTIONS` (same file) — tools the registry registers
  outside the catalogue;
* `REGISTRY_ONLY_TOOL_NAMES` / `TOOLS_OUTSIDE_DEFINITIONS`
  (`src/executor/mod.rs`) — the names `is_builtin_tool_name` accepts;
* `BRIDGE_TOOL_DESCRIPTIONS` / `INJECTED_TOOL_DESCRIPTIONS` (same file) —
  the MCP bridge tools and the per-request injected tools;
* `reg(tools, "...")` in `src/executor/builtin_registry/builder/` — the
  conditional registration sites;
* `tool_search` (`src/tools/tool_search.rs`) and `get_tool_schema`
  (`src/tools/schema_lookup.rs`).

Reading the lists rather than sweeping the tree keeps the census free of
test fixtures (`fake_tool`, `stub`, `panic`, …) and free of the
`#[cfg(test)]` stripping that a sweep would need.

The docs side is every place the site presents an identifier *as a tool
name*: the first cell of a table whose header names tools, and the explicit
`tool_use("...")` / `allows_tool("...")` call sites.

Two failure modes are reported:

* ghost  — a tool name the docs present that the code never registers
  (a renamed tool, a module name mistaken for a tool, a fabricated name);
* missing — a registered tool no page mentions.

A baseline file records the known set so that adding a tool to the code does
not fail the gate until the docs catch up (and removing one does not fail it
until the docs drop it).

Usage:
    python3 scripts/tool_audit.py --repo ../Aleph --docs content/docs
    python3 scripts/tool_audit.py --repo ../Aleph --docs content/docs --json
    python3 scripts/tool_audit.py --repo ../Aleph --docs content/docs --update-baseline
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gate_baseline import load_baseline, split_violations, update_section  # noqa: E402

# --- code side ---------------------------------------------------------------

# 注册面所在的文件（每个都对应代码里一份「这是真的工具」的权威名单）。
DEFINITIONS_FILE = "src/executor/builtin_registry/definitions.rs"
EXECUTOR_FILE = "src/executor/mod.rs"
BUILDER_DIR = "src/executor/builtin_registry/builder"
TOOL_SEARCH_FILE = "src/tools/tool_search.rs"
SCHEMA_LOOKUP_FILE = "src/tools/schema_lookup.rs"

# `const NAME: &'static str = "..."` 只在两个「按请求注入」的工具上读：
# 它们不在任何目录里，但确实是模型能调用的工具。
INJECTED_NAME_RE = re.compile(r'''const\s+NAME\s*:\s*&'static\s+str\s*=\s*"([a-z][a-z0-9_]*)"''')

# `reg(tools, "name", …)` —— 注册表的条件注册点。
REG_CALL_RE = re.compile(r'reg\(\s*tools,\s*"([a-z][a-z0-9_]*)"')

# `crate::a::b::CONST` 形式的引用（工具名以常量的方式被引用）。
CONST_REF_RE = re.compile(r'crate::[A-Za-z0-9_:]+')

# --- docs side ---------------------------------------------------------------

# 表格首列被当作工具名的条件：表头里必须有一格明确在说「工具」。
TOOL_HEADER_RE = re.compile(
    r"^(工具|工具名|内建工具|内置工具|内置工具（.*）|工具（.*）|tool|tools|tool name|tool names|builtin tool|built-in tool|built-in tools)$",
    re.IGNORECASE,
)
TOKEN_RE = re.compile(r"`([a-z][a-z0-9_]*)`")
CALL_SITE_RE = re.compile(r'''(?:tool_use|allows_tool|tool_call|invoke_tool)\(\s*"([a-z][a-z0-9_]*)"''')

# 明确不是 Aleph 内置工具的名字，各自写明理由。
# 门禁不能因为站点提到一个 Rust crate 或一个示例名就报幽灵。
EXEMPT_NAMES: dict[str, str] = {
    # 第四轮校准后不再需要任何豁免：
    # - dev-dependency crate 所在的表头已从「工具 | 用途」改成
    #   「命令 / crate | 用途」，不再是工具声明表；
    # - `concepts/identity-context.mdx` 的访客示例改用真实工具名
    #   `code_exec`，不再用假想名。
    # 新增豁免前先想清楚：能不能改文档本身来消除这条声明。
}

# --- helpers -----------------------------------------------------------------


def strip_cfg_test(text: str) -> str:
    """Remove `#[cfg(test)] mod ... { ... }` blocks from a Rust source file."""
    out: list[str] = []
    index = 0
    length = len(text)
    while index < length:
        marker = text.find("#[cfg(test)]", index)
        if marker == -1:
            out.append(text[index:])
            break
        out.append(text[index:marker])
        # 只有「`#[cfg(test)] mod … { … }`」才是可以整块剥掉的测试模块。
        # `#[cfg(test)]` 也可能标在单个函数或常量上——那时**不能**往后找
        # `mod`，否则会把后面成千上万行生产代码一起吃掉（本轮踩过：
        # `src/builtin_tools/memory_search.rs` 的 `#[cfg(test)]` 在第 236 行，
        # 而 `const NAME` 在第 272 行）。
        module = re.compile(r"\s*(?:pub\s+)?mod\s+\w+\s*\{").match(text, marker + len("#[cfg(test)]"))
        if not module:
            out.append("#[cfg(test)]")
            index = marker + len("#[cfg(test)]")
            continue
        brace = module.end() - 1
        depth = 0
        end = length
        for position in range(brace, length):
            if text[position] == "{":
                depth += 1
            elif text[position] == "}":
                depth -= 1
                if depth == 0:
                    end = position + 1
                    break
        index = end
    return "".join(out)


def is_test_file(path: Path) -> bool:
    name = path.name
    return (
        name.endswith("_tests.rs")
        or name.endswith("_test.rs")
        or name == "tests.rs"
        or "tests" in path.parts
    )


def _table(text: str, name: str) -> str:
    """The body of a Rust `const NAME: &[...] = &[ ... ];` table."""
    index = text.find(name)
    if index == -1:
        return ""
    end = text.find("];", index)
    return text[index:end] if end != -1 else text[index:]


def _resolve_const(repo: Path, reference: str) -> str | None:
    """Resolve `crate::a::b::CONST` to the string it holds."""
    parts = reference.split("::")
    constant = parts[-1]
    if len(parts) < 3:
        return None
    module = Path(*parts[1:-1])
    candidates = [repo / "src" / module.with_suffix(".rs"), repo / "src" / module / "mod.rs"]
    for candidate in candidates:
        if not candidate.exists():
            continue
        text = candidate.read_text(encoding="utf-8", errors="ignore")
        pattern = re.compile(
            r"const\s+" + re.escape(constant) + r"\s*:\s*&(?:'static\s+)?str\s*=\s*\"([^\"]+)\""
        )
        found = pattern.search(text)
        if found:
            return found.group(1)
    return None


def census_tools(repo: Path) -> set[str]:
    """Every builtin tool name the code registers.

    The lists read here are the code's own: the catalogue
    (`BUILTIN_TOOL_DEFINITIONS`), the registry-only names, the names
    `is_builtin_tool_name` accepts, the MCP bridge and injected tables, the
    conditional registration sites, and the two tools that are pushed into
    each request rather than registered globally.
    """
    found: set[str] = set()

    definitions_path = repo / DEFINITIONS_FILE
    if definitions_path.exists():
        text = definitions_path.read_text(encoding="utf-8", errors="ignore")
        catalogue = _table(text, "BUILTIN_TOOL_DEFINITIONS")
        found.update(re.findall(r'name:\s*"([^"]+)"', catalogue))
        registry_only = _table(text, "REGISTRY_ONLY_DESCRIPTIONS")
        found.update(re.findall(r'\(\s*"([a-z][a-z0-9_]*)"\s*,', registry_only))
        for table in ("BRIDGE_TOOL_DESCRIPTIONS", "INJECTED_TOOL_DESCRIPTIONS"):
            for reference in set(CONST_REF_RE.findall(_table(text, table))):
                resolved = _resolve_const(repo, reference)
                if resolved and re.fullmatch(r"[a-z][a-z0-9_]*", resolved):
                    found.add(resolved)

    executor_path = repo / EXECUTOR_FILE
    if executor_path.exists():
        text = executor_path.read_text(encoding="utf-8", errors="ignore")
        names = _table(text, "REGISTRY_ONLY_TOOL_NAMES")
        found.update(re.findall(r'^\s*"([a-z][a-z0-9_]*)",?\s*$', names, re.M))
        outside = _table(text, "TOOLS_OUTSIDE_DEFINITIONS")
        for reference in set(CONST_REF_RE.findall(outside)):
            resolved = _resolve_const(repo, reference)
            if resolved and re.fullmatch(r"[a-z][a-z0-9_]*", resolved):
                found.add(resolved)
        for constant in re.findall(r'crate::[A-Za-z0-9_:]*::NAME', outside):
            resolved = _resolve_const(repo, constant.rsplit("::", 1)[0] + "::NAME")
            if resolved and re.fullmatch(r"[a-z][a-z0-9_]*", resolved):
                found.add(resolved)

    builder = repo / BUILDER_DIR
    if builder.exists():
        for path in sorted(builder.rglob("*.rs")):
            if is_test_file(path):
                continue
            found.update(
                REG_CALL_RE.findall(path.read_text(encoding="utf-8", errors="ignore"))
            )

    for relative in (TOOL_SEARCH_FILE, SCHEMA_LOOKUP_FILE):
        path = repo / relative
        if not path.exists():
            continue
        found.update(
            INJECTED_NAME_RE.findall(path.read_text(encoding="utf-8", errors="ignore"))
        )

    return found


def table_rows(lines: list[str]) -> list[tuple[int, list[str], list[str]]]:
    """Yield (line number, header cells, body cells) for every markdown table."""
    rows: list[tuple[int, list[str], list[str]]] = []
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if (
            stripped.startswith("|")
            and index + 1 < len(lines)
            and set(lines[index + 1].strip().strip("|").replace("|", "").replace(" ", ""))
            <= set("-:")
            and lines[index + 1].strip().startswith("|")
        ):
            header = [cell.strip() for cell in stripped.strip("|").split("|")]
            body: list[str] = []
            cursor = index + 2
            while cursor < len(lines) and lines[cursor].strip().startswith("|"):
                body.append(lines[cursor].strip())
                cursor += 1
            rows.append((index + 1, header, body))
            index = cursor
            continue
        index += 1
    return rows


def doc_tool_mentions(docs: Path, only: set[str] | None = None) -> tuple[dict[str, set[str]], dict[str, str]]:
    """Every identifier the pages mention, and the raw text of every page.

    This is the *coverage* side of the census: a registered tool counts as
    documented as soon as one page mentions it by name, no matter where.
    Two mention shapes count:

    * a backticked token (`workspace_manage`);
    * a plain occurrence in prose (`workspace_manage` inside a sentence).

    The changelog is skipped: it records what a past release said, not what
    the current pages describe.
    """
    mentions: dict[str, set[str]] = {}
    corpus: dict[str, str] = {}
    for path in sorted(docs.rglob("*.mdx")):
        if path.name == "changelog.mdx":
            continue
        relative = str(path.relative_to(docs))
        if only is not None and relative not in only:
            continue
        text = path.read_text(encoding="utf-8")
        corpus[relative] = text
        for token in TOKEN_RE.findall(text):
            mentions.setdefault(token, set()).add(relative)
    return mentions, corpus


def doc_tool_claims(docs: Path, only: set[str] | None = None) -> dict[str, set[str]]:
    """Tool names the documentation presents, grouped by the pages that do it.

    Two claim shapes are recognised:

    * a table whose header names tools — the first cell of each body row is
      read as a tool name (the convention used by the tool catalogues);
    * an explicit call site — `tool_use("x")`, `allows_tool("x")`.
    """
    claims: dict[str, set[str]] = {}
    for path in sorted(docs.rglob("*.mdx")):
        if path.name == "changelog.mdx":
            continue
        relative = str(path.relative_to(docs))
        if only is not None and relative not in only:
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        for _, header, body in table_rows(lines):
            if not any(TOOL_HEADER_RE.match(cell) for cell in header):
                continue
            for row in body:
                cells = [cell.strip() for cell in row.strip("|").split("|")]
                if not cells:
                    continue
                for token in TOKEN_RE.findall(cells[0]):
                    claims.setdefault(token, set()).add(relative)
        for match in CALL_SITE_RE.finditer(text):
            claims.setdefault(match.group(1), set()).add(relative)
    return claims


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="../Aleph", type=Path)
    parser.add_argument("--docs", default="content/docs", type=Path)
    parser.add_argument("--baseline", default=str(Path(__file__).resolve().parent / "baseline.json"))
    parser.add_argument("--update-baseline", action="store_true", help="把当前失效集合写回基线（棘轮）")
    parser.add_argument("--files", default="", help="逗号分隔的页面相对路径（相对 docs 根），只审计这些页")
    parser.add_argument("--files-from", type=Path, default=None, help="每行一个页面相对路径的文件")
    parser.add_argument("--raw", action="store_true", help="不做基线拆分，直接输出全部 ghost/missing")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    scope: set[str] | None = None
    listed = [item.strip() for item in args.files.split(",") if item.strip()]
    if args.files_from and args.files_from.exists():
        listed += [line.strip() for line in args.files_from.read_text(encoding="utf-8").splitlines() if line.strip()]
    if listed:
        scope = set(listed)

    registered = census_tools(args.repo)
    claimed = doc_tool_claims(args.docs, scope)
    mentioned, corpus = doc_tool_mentions(args.docs, scope)

    exempt = {name for name in claimed if name in EXEMPT_NAMES}
    ghost = sorted(
        name
        for name in claimed
        if name not in registered and name not in EXEMPT_NAMES
    )
    # 「已注册未文档化」：页面里既没有反引号形式，也没有任何正文出现。
    missing_locations: dict[str, set[str]] = {}
    missing: list[str] = []
    for name in sorted(registered):
        pages = set(mentioned.get(name, set()))
        for relative, text in corpus.items():
            if name in text:
                pages.add(relative)
        if not pages:
            missing.append(name)
        else:
            missing_locations[name] = pages

    if args.raw:
        payload = {
            "scope_files": sorted(scope) if scope else "all",
            "registered_tools": len(registered),
            "documented_claims": len(claimed),
            "ghost": ghost,
            "ghost_locations": {name: sorted(claimed[name]) for name in ghost},
            "missing": missing,
            "missing_locations": {name: sorted(missing_locations.get(name, set())) for name in missing},
            "exempt": sorted(exempt),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else "\n".join(
            [f"registered tools: {len(registered)}   documented claims: {len(claimed)}"]
            + [f"ghost ({len(ghost)}):"]
            + [f"  {name}  <- {', '.join(sorted(claimed[name]))}" for name in ghost]
            + [f"missing ({len(missing)}):"]
            + [f"  {name}" for name in missing]
            + [f"exempt ({len(exempt)}): " + ", ".join(sorted(exempt))]
        ))
        return 0

    baseline = load_baseline(Path(args.baseline))
    new_ghost, known_ghost = split_violations(ghost, baseline.get("tool_ghost", []))
    new_missing, known_missing = split_violations(missing, baseline.get("tool_missing", []))

    if args.update_baseline:
        fixed = update_section("tool_ghost", ghost, Path(args.baseline))
        fixed += update_section("tool_missing", missing, Path(args.baseline))
        print(f"基线已棘轮：tool_ghost {len(ghost)} 条，tool_missing {len(missing)} 条，修掉 {len(fixed)} 条")
        for item in fixed:
            print(f"  FIXED {item}")
        new_ghost, known_ghost = [], ghost
        new_missing, known_missing = [], missing

    if args.json:
        print(json.dumps({
            "registered_tools": len(registered),
            "documented_claims": len(claimed),
            "new_ghost": new_ghost,
            "new_missing": new_missing,
            "known_ghost": known_ghost,
            "known_missing": known_missing,
            "ghost_locations": {name: sorted(claimed[name]) for name in ghost},
            "missing_locations": {name: sorted(missing_locations.get(name, set())) for name in missing},
        }, ensure_ascii=False, indent=2))
    else:
        print(f"registered builtin tools: {len(registered)}   documented tool claims: {len(claimed)}")
        print(f"ghost (documented, not registered): {len(ghost)}（新增 {len(new_ghost)}，基线旧债 {len(known_ghost)}）")
        for name in new_ghost:
            for location in sorted(claimed[name]):
                print(f"  GHOST {name}  <- {location}")
        print(f"missing (registered, undocumented): {len(missing)}（新增 {len(new_missing)}，基线旧债 {len(known_missing)}）")
        for name in new_missing:
            print(f"  MISSING {name}")

    return 1 if (new_ghost or new_missing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
