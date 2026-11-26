#!/usr/bin/env python3
"""Method census audit: compare documented JSON-RPC methods against the code.

The code side is two sources in the Aleph repo:

* `src/gateway/method_census.rs` pins one role ruling (Open / Admin) per
  registered gateway RPC method;
* every dotted string literal in the workspace is treated as a known topic or
  event name, so that server-to-client events documented in prose are not
  mistaken for removed RPC methods.

The docs side is every backticked dotted token in the documentation site's
content.

Two failure modes are reported:

* ghost  — a method the docs document that appears nowhere in the code;
* missing — a registered method no page mentions.

A baseline file records the known set so that adding a method to the code does
not fail the gate until the docs catch up (and removing one does not fail it
until the docs drop it).

Usage:
    python3 scripts/method_audit.py --repo ../Aleph --docs content/docs
    python3 scripts/method_audit.py --repo ../Aleph --docs content/docs --json
    python3 scripts/method_audit.py --repo ../Aleph --docs content/docs --update-baseline
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gate_baseline import load_baseline, split_violations, update_section  # noqa: E402

CENSUS_RE = re.compile(r'\(\s*"([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)"\s*,\s*Class::(Admin|Open)')
# 部分 census 条目不是字面量，而是协议 crate 里的常量，例如
# `aleph_protocol::chat_transcript::CHAT_TRANSCRIPT_DETAILS_METHOD`。
# 只认字面量的门会让这类方法凭空消失：注册了，却永远不会被判成「已注册未文档化」。
CENSUS_CONST_RE = re.compile(
    r'\(\s*([A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z_][A-Za-z0-9_]*)+)\s*,\s*Class::(Admin|Open)\s*,?\s*\)',
    re.S,
)
CONST_VALUE_RE = re.compile(r'pub\s+const\s+([A-Z][A-Z0-9_]+)\s*:\s*&str\s*=\s*"([^"]+)"')
DOC_TOKEN_RE = re.compile(r"`([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)`")
NON_METHOD_SUFFIXES = (".rs", ".toml", ".md", ".mdx", ".json", ".js", ".ts", ".tsx", ".yml", ".yaml")
# 这些前缀是**源码/文档路径**，不是 RPC 方法名。注意 `config.` 不在此列：
# `config.get` / `config.schema` / `config.reload` 是真实的方法命名空间。
NON_METHOD_PREFIXES = ("src.", "desktop.", "shared.", "crates.", "interfaces.", "docs.", "scripts.", "qa.", "tests.", "content.")

# 协议消息与描述符的**字段路径**，不是 RPC 方法名。协议页与能力页按结构写字段，
# 例如 `limits.max_message_bytes`（JSON）或 `schema.fingerprint`（Rust 结构体）。
# 这些前缀与 census 的方法命名空间不重叠，按前缀排除不会漏掉真的方法幽灵。
FIELD_PATH_PREFIXES = (
    "limits.",
    "result.",
    "params.",
    "client.",
    "server.",
    "protocol.",
    "features.",
    "error.",
    "data.",
    "jsonrpc.",
    "notification.",
    "hello.",
    "message.",
    "code.",
    "version.",
    "name.",
    "platform.",
    "ui_runtime.",
    "schema.",
)

# 文件名与浏览器全局：带扩展名或 JS 全局前缀，不是方法名。
FILE_EXTENSION_SUFFIXES = (
    ".wasm", ".js", ".mjs", ".ts", ".tsx", ".css", ".html", ".rs", ".toml",
    ".json", ".md", ".mdx", ".png", ".svg", ".zip", ".tar", ".gz", ".txt", ".lock",
)
BROWSER_GLOBAL_PREFIXES = (
    "location.", "window.", "document.", "navigator.", "console.",
    "globalThis.", "process.", "localStorage.", "sessionStorage.", "import.meta.",
)

# **否定与历史语境**：这些行是在说明某个方法「不存在 / 已废弃 / 已被取代 / 是旧名」，
# 不是在宣称站点提供了这个方法。方法册要抓的是「文档宣称存在但 census 里没有」，
# 所以这些行里的点号标识符不算幽灵。
NEGATION_MARKERS = (
    # 中文
    "没有登记", "未登记", "未注册", "不存在", "尚未存在", "没有这个", "并没有", "不再",
    "已废弃", "已移除", "已删除", "已取代", "取代了", "旧名", "旧的事件名",
    "早期文档", "早期计划", "历史上", "曾经", "曾用", "旧版", "老名字",
    "并非", "不是方法", "不是方法名", "别称", "别名",
    # English（注意不要用裸 "histor" / "removed"：会误伤 `chat.history` 这类方法名）
    "not registered", "does not exist", "doesn't exist", "not exist",
    "no longer", "previously", "legacy", "historical", "historically",
    "deprecated", "was removed", "were removed", "has been removed",
    "renamed", "superseded", "obsolete", "not a method",
    "former name", "old name", "old event", "old event name",
    "not registered", "not currently registered", "is not registered",
    "not exist", "not currently exist",
)

# `config.` 是真实的 RPC 命名空间（config.get / config.schema / config.reload …），
# 不能整体排除；但命名空间下也有**不是**方法的东西，逐个列出：
CONFIG_NON_METHODS = {
    # Rust 函数名（配置模块内部），不是 RPC 方法
    "config.get_full_config",
    "config.reload_with_subsystems",
    # 配置文件里的键 / 路径
    "config.enabled",
    "config.policies.capability_constraints",
    "config.policies",
}


def code_literals(repo: Path) -> set[str]:
    """Every dotted string literal in the workspace: topics, events, method names."""
    literal_re = re.compile(r'"([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)"')
    found: set[str] = set()
    for root in ("src", "shared", "interfaces", "desktop", "crates"):
        base = repo / root
        if not base.exists():
            continue
        for path in base.rglob("*.rs"):
            if ".worktrees" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in literal_re.findall(text):
                if token.endswith(NON_METHOD_SUFFIXES):
                    continue
                found.add(token)
    return found


def protocol_constants(repo: Path) -> dict[str, str]:
    """`pub const NAME: &str = "..."` 的常量名 → 字符串值。

    只扫描协议与实现 crate 的源码目录；常量值即 RPC 方法名。
    """
    found: dict[str, str] = {}
    for root in ("shared", "src", "interfaces", "desktop", "crates"):
        base = repo / root
        if not base.exists():
            continue
        for path in base.rglob("*.rs"):
            if ".worktrees" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for name, value in CONST_VALUE_RE.findall(text):
                found.setdefault(name, value)
    return found


def census_methods(repo: Path) -> dict[str, str]:
    path = repo / "src" / "gateway" / "method_census.rs"
    if not path.exists():
        sys.exit(f"census not found: {path}")
    text = path.read_text(encoding="utf-8")
    found: dict[str, str] = {}
    for name, cls in CENSUS_RE.findall(text):
        found[name] = cls.lower()
    constants = protocol_constants(repo)
    for path_expr, cls in CENSUS_CONST_RE.findall(text):
        const_name = path_expr.split("::")[-1]
        value = constants.get(const_name)
        if value is None:
            continue
        found.setdefault(value, cls.lower())
    return found


def doc_methods(docs: Path, only: set[str] | None = None, namespaces: set[str] | None = None) -> dict[str, set[str]]:
    """Backticked dotted identifiers in the docs, grouped by page.

    `namespaces` is the set of RPC namespace prefixes taken from the method
    census. A dotted identifier whose first segment is not a known namespace is
    a configuration key, a struct field path, a URL or a file name — not an RPC
    method — so it is not a "ghost".

    `changelog.mdx` is exempt: it is a historical record and legitimately names
    methods that have since been retired or renamed.
    """
    hits: dict[str, set[str]] = {}
    for path in sorted(docs.rglob("*.mdx")):
        if path.name == "changelog.mdx":
            continue
        if only is not None and str(path.relative_to(docs)) not in only:
            continue
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            low = line.lower()
            if any(marker in low for marker in NEGATION_MARKERS):
                continue
            for token in DOC_TOKEN_RE.findall(line):
                if token.endswith(NON_METHOD_SUFFIXES):
                    continue
                if token.startswith(NON_METHOD_PREFIXES):
                    continue
                if token.startswith(FIELD_PATH_PREFIXES):
                    continue
                if token.endswith(FILE_EXTENSION_SUFFIXES):
                    continue
                if token.startswith(BROWSER_GLOBAL_PREFIXES):
                    continue
                if token in CONFIG_NON_METHODS:
                    continue
                if namespaces is not None and token.split(".", 1)[0] not in namespaces:
                    continue
                hits.setdefault(token, set()).add(str(path))
    return hits


def load_baseline_unused(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {"ghost": [], "missing": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {"ghost": sorted(data.get("ghost", [])), "missing": sorted(data.get("missing", []))}


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
    listed = [p.strip() for p in args.files.split(",") if p.strip()]
    if args.files_from and args.files_from.exists():
        listed += [ln.strip() for ln in args.files_from.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if listed:
        scope = set(listed)

    real = census_methods(args.repo)
    known = set(real) | code_literals(args.repo)
    namespaces = {name.split(".", 1)[0] for name in real}
    documented = doc_methods(args.docs, scope, namespaces)

    ghost = sorted(set(documented) - known)
    missing = sorted(set(real) - set(documented))

    if args.raw:
        print(json.dumps({
            "scope_files": sorted(scope) if scope else "all",
            "ghost": ghost,
            "ghost_locations": {m: sorted(documented[m]) for m in ghost},
            "missing": missing,
        }, ensure_ascii=False, indent=2) if args.json else
            "\n".join(
                [f"ghost ({len(ghost)}):"]
                + [f"  {m}  <- {', '.join(sorted(documented[m]))}" for m in ghost]
                + [f"missing ({len(missing)}):"]
                + [f"  {m}" for m in missing]
            ))
        return 0

    baseline = load_baseline(Path(args.baseline))
    new_ghost, known_ghost = split_violations(ghost, baseline.get("method_ghost", []))
    new_missing, known_missing = split_violations(missing, baseline.get("method_missing", []))

    if args.update_baseline:
        fixed = update_section("method_ghost", ghost, Path(args.baseline))
        fixed += update_section("method_missing", missing, Path(args.baseline))
        print(f"基线已棘轮：method_ghost {len(ghost)} 条，method_missing {len(missing)} 条，修掉 {len(fixed)} 条")
        for item in fixed:
            print(f"  FIXED {item}")
        new_ghost, known_ghost = [], ghost
        new_missing, known_missing = [], missing

    if args.json:
        print(json.dumps({
            "census_methods": len(real),
            "documented_tokens": len(documented),
            "new_ghost": new_ghost,
            "new_missing": new_missing,
            "known_ghost": known_ghost,
            "known_missing": known_missing,
            "ghost_locations": {m: sorted(documented[m]) for m in ghost},
        }, ensure_ascii=False, indent=2))
    else:
        print(f"census methods: {len(real)}   documented dotted tokens: {len(documented)}")
        print(f"ghost (documented, absent from code): {len(ghost)}（新增 {len(new_ghost)}，基线旧债 {len(known_ghost)}）")
        for method in new_ghost:
            for location in sorted(documented[method]):
                print(f"  GHOST {method}  <- {location}")
        print(f"missing (registered, undocumented): {len(missing)}（新增 {len(new_missing)}，基线旧债 {len(known_missing)}）")
        for method in new_missing:
            print(f"  MISSING {method}")

    return 1 if (new_ghost or new_missing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
