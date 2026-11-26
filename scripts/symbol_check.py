#!/usr/bin/env python3
"""符号门（G1c）：文档里写的代码符号、crate 名、`just` 目标必须在真实仓库里存在。

用法：
    python3 scripts/symbol_check.py [--repo ../Aleph] [--docs content/docs]
    python3 scripts/symbol_check.py --repo ../Aleph --json > symbols.json

为什么需要这道门：
    G1（anchor_check.py）只管**路径**。重构把一个函数、类型或常量改名时，路径还在，
    文档却开始说一个已经不存在的名字——这类腐化是站点第二轮对齐的主要形态。
    本门把 Aleph 代码仓 `scripts/doc_wiring_audit.py` 的 SYMBOLS / CRATES / JUST
    三项检查移植到文档站，覆盖 328 个页面的反引号 token。

判定规则：
  * 只检查反引号包裹、形似代码符号的 token：含 `::`、以 `()` 结尾、
    小写下划线且长度 > 4、或至少两个驼峰（如 `PanelShell`）。
  * 符号集合来自 Aleph 仓 `git ls-files` 收录的源码文件里出现过的全部标识符。
  * `## 历史：…` / `## 规划中：…` 小节里的 token 免检（那两节按约定描述
    「当时」或「将来」，不要求当下存在）。
  * crate 形状（`aleph-*`）的 token 必须在 Cargo.toml 里是真包名。
  * `just <target>` 必须在 Aleph 仓的 justfile 里有同名 recipe。

退出码：0 = 没有基线之外的新失效（基线里的旧债只提示）；1 = 出现新失效。

基线：`scripts/baseline.json` 的 `symbol` 段。修完一段债务后用
`--update-baseline` 棘轮，新出现的失效立即让门变红。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gate_baseline import load_baseline, split_violations, update_section  # noqa: E402
from gate_exempt import exempt_lines  # noqa: E402

CODE_RE = re.compile(r"`([^`\n]+)`")
SYMBOL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z_][A-Za-z0-9_]*)*)(?:\(\))?$")
CAMEL_RE = re.compile(r"^[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+$")
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
# 双下划线是 Rust 符号改写或工具名拼接的产物，不是可对照的标识符。
DOUBLE_UNDERSCORE_RE = re.compile(r"__")
SOURCE_RE = re.compile(r"(\.(rs|ts|tsx|js|mjs|cjs|py|swift|sh|toml|json|yml|yaml)|justfile)$")
JUST_RE = re.compile(r"\bjust\s+([a-zA-Z0-9_-]+)")
CRATE_RE = re.compile(r"^aleph-[a-z0-9]+(?:-[a-z0-9]+)*$")
# 看起来像 crate、其实不是 Rust crate 的名字。`aleph-bridge` 是 Swift helper
# 的可执行文件名（`desktop/macos/bridge/` 的 Swift package 名是 `AlephBridge`，
# justfile 只把产物软链成 `aleph-bridge`），仓库里没有同名 crate。
CRATE_ALIASES = {
    "aleph-bridge",
}
# 判定「这个 token 被当成 crate 说」的距离窗口：crate 字样必须紧邻 token，
# 且中间不能跨句。用 120 字符窗口会把同一段里别的主语也算进来
# （例如 Swift CLI 附近的 "Swift package"）。
CRATE_MENTION_RE = re.compile(r"\b(crate|package|workspace member|workspace crate)s?\b")
CRATE_MENTION_MAX_DISTANCE = 40
CRATE_SENTENCE_BREAKS = "。；;！!？?\n"

# 站点自己造的词、协议名等：形状像符号但不是代码里的标识符。
SYMBOL_ALLOWLIST = {
    "crate",
    "self",
    "super",
    "std",
    "Tauri",
    "NSH",
    "TSX",
    "IPC",
    "JSON",
    "JSON-RPC",
    "WebSocket",
    "WebSockets",
    "Rust",
    "Leptos",
    "React",
    "TypeScript",
    "JavaScript",
    "WASM",
    "Wasm",
    "TOML",
    "YAML",
    "JSON-RPC",
    "Unicode",
    "UTF-8",
    "CLI",
    "GUI",
    "HTTP",
    "HTTPS",
    "TLS",
    "TCP",
    "UDP",
    "DNS",
    "URL",
    "URI",
    "UUID",
    "SSE",
    "MCP",
    "A2A",
    "ACP",
    "LSP",
    "PDF",
    "Markdown",
    "TOML",
    "SQL",
    "SQLite",
    "GPU",
    "CPU",
    "IPC",
    "OS",
    "BSD",
    "Unix",
    "Linux",
    "macOS",
    "Windows",
    "iOS",
    "Android",
    "Rust",
    "TypeScript",
    "Python",
    "Bash",
    "Zsh",
    "Fish",
    "TOML",
    "SSH",
    "TLS",
}


def known_symbols(repo: Path) -> set[str]:
    """Aleph 仓源码里出现过的全部标识符。"""
    listed = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--recurse-submodules"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    names: set[str] = set()
    for rel in listed:
        if not SOURCE_RE.search(rel):
            continue
        path = repo / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        names.update(IDENT_RE.findall(text))
    return names


def known_crates(repo: Path) -> set[str]:
    """Aleph 仓里真实存在的 crate（package）名。"""
    names: set[str] = set()
    for rel in subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--recurse-submodules", "*/Cargo.toml", "Cargo.toml"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines():
        path = repo / rel
        if not path.is_file():
            continue
        section: str | None = None
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.strip()
            if stripped.startswith("["):
                section = stripped.strip("[]")
                continue
            if section not in ("package", "bin"):
                continue
            if stripped.startswith("name"):
                value = stripped.split("=", 1)[1].strip().strip('"').strip("'")
                if value:
                    names.add(value)
    return names


def known_just_targets(repo: Path) -> set[str]:
    """justfile 里定义的 recipe 名。"""
    targets: set[str] = set()
    for name in ("justfile", "Justfile", ".justfile"):
        path = repo / name
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            match = re.match(r"^([a-zA-Z0-9_.-]+):", line)
            if match:
                targets.add(match.group(1))
    return targets


def claims_crate(text: str, start: int, end: int) -> bool:
    """True when the token is itself called a crate / package / workspace member.

    The crate word has to sit right next to the token and stay inside the same
    sentence. A wider window misattributes neighbouring subjects: the macOS
    bridge page says "the Swift package lives in ...", and the `aleph-bridge`
    binary name sits in that same paragraph without ever being a crate.
    """
    for match in CRATE_MENTION_RE.finditer(text):
        if match.end() <= start:
            gap = text[match.end() : start]
            distance = len(gap)
        elif match.start() >= end:
            gap = text[end : match.start()]
            distance = len(gap)
        else:
            distance = 0
            gap = ""
        if distance > CRATE_MENTION_MAX_DISTANCE:
            continue
        if any(break_char in gap for break_char in CRATE_SENTENCE_BREAKS):
            continue
        return True
    return False


def symbol_candidates(text: str):
    """反引号里形似代码符号的 token，连同行号。"""
    flags = exempt_lines(text)
    for index, line in enumerate(text.splitlines()):
        if flags[index]:
            continue
        for span in CODE_RE.finditer(line):
            token = span.group(1).strip()
            match = SYMBOL_RE.match(token)
            if not match:
                continue
            if DOUBLE_UNDERSCORE_RE.search(token):
                continue
            segments = match.group(1).split("::")
            last = segments[-1]
            snake = "_" in last and last == last.lower() and len(last) > 4
            if "::" in token or token.endswith("()") or snake or CAMEL_RE.match(last):
                yield token, segments


def main() -> int:
    parser = argparse.ArgumentParser(description="Aleph 文档符号门")
    parser.add_argument("--repo", default="../Aleph", help="Aleph 代码仓路径")
    parser.add_argument("--docs", default="content/docs", help="文档内容根（相对文档仓）")
    parser.add_argument("--docs-repo", default=".", help="文档仓自身路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument(
        "--baseline", default=str(Path(__file__).resolve().parent / "baseline.json")
    )
    parser.add_argument("--update-baseline", action="store_true", help="把当前失效集合写回基线（棘轮）")
    args = parser.parse_args()

    docs_repo = Path(args.docs_repo).resolve()
    repo = Path(args.repo).resolve()
    content_root = (docs_repo / args.docs).resolve()

    if not content_root.is_dir():
        print(f"找不到文档内容目录：{content_root}", file=sys.stderr)
        return 2
    if not repo.is_dir():
        print(f"找不到代码仓：{repo}", file=sys.stderr)
        return 2

    symbols = known_symbols(repo)
    crates = known_crates(repo)
    just_targets = known_just_targets(repo)

    violations: list[str] = []
    skipped = 0

    for page in sorted(content_root.rglob("*.mdx")):
        rel = page.relative_to(content_root)
        text = page.read_text(encoding="utf-8", errors="ignore")
        for token, segments in symbol_candidates(text):
            if token in SYMBOL_ALLOWLIST:
                continue
            missing = [s for s in segments if s not in symbols]
            if missing:
                violations.append(f"{rel}: 符号不存在：{token}（缺 {'/'.join(missing)}）")
        # crate 名：形如 aleph-xxx 的 token 必须是真 crate
        for span in CODE_RE.finditer(text):
            token = span.group(1).strip().rstrip(".,;:")
            if not CRATE_RE.match(token):
                continue
            if token in crates or token in CRATE_ALIASES:
                continue
            mentions_crate = claims_crate(text, span.start(), span.end())
            cargo_command = re.search(rf"cargo\b[^\n]*\b{re.escape(token)}\b", text)
            if mentions_crate or cargo_command:
                violations.append(f"{rel}: crate 不存在：{token}")
            else:
                skipped += 1
        # just 目标：`just xxx` 必须在 justfile 里有同名 recipe
        for span in CODE_RE.finditer(text):
            for target in JUST_RE.findall(span.group(1)):
                if target not in just_targets:
                    violations.append(f"{rel}: just 目标不存在：just {target}")

    baseline_path = Path(args.baseline)
    baseline = load_baseline(baseline_path)
    known = baseline.get("symbol", [])

    if args.update_baseline:
        dropped = update_section("symbol", violations, baseline_path)
        for item in dropped:
            print(f"已修复：{item}")

    new, old = split_violations(violations, known)

    if args.json:
        print(json.dumps({"new": new, "known": old}, ensure_ascii=False, indent=2))
    else:
        total = len(violations)
        print(
            f"页面 {len(list(content_root.rglob('*.mdx')))}，失效 {total}"
            f"（新增 {len(new)}，基线旧债 {len(old)}）"
        )
        for item in new:
            print(f"NEW  {item}")
        for item in old:
            print(f"OLD  {item}")

    return 1 if new else 0


if __name__ == "__main__":
    raise SystemExit(main())
