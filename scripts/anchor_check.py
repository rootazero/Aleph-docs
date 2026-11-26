#!/usr/bin/env python3
"""锚点门（G1）：文档里写的源码路径必须在真实仓库里存在。

用法：
    python3 scripts/anchor_check.py [--repo ../Aleph] [--docs content/docs]
    python3 scripts/anchor_check.py --repo ../Aleph --json > anchors.json

判定规则：
  * 只检查反引号包裹、且以已知源码根开头的 token（src/ desktop/ shared/ crates/
    interfaces/ plugins/ scripts/ qa/ tests/ docs/），以及少量根文件名。
  * 裸文件名（不含目录、以 .rs / .py 结尾）另有一道检查：仓库里必须能找到同名文件。
  * 含占位符（{} * < > $ …）的 token 视为通配，跳过并计入 skipped。
  * 「历史 / 规划中」小节里的 token 免检：那两节按约定描述当时与将来的状态，
    路径可能已经被删掉，也可能还不存在。免检规则与符号门
    （scripts/symbol_check.py 的 EXEMPT_HEADING_RE）保持一致，中英文对称。
  * 结尾是 / 的按目录判定，其余按文件判定。
  * `::symbol`、`#anchor` 后缀先剥掉再判定路径。

退出码：0 = 没有新的失效锚点（基线里的旧债只提示）；1 = 出现基线之外的新失效锚点。

基线：`scripts/baseline.json` 的 `anchor` 段。修完一段债务后用
`--update-baseline` 把基线往下棘轮，新出现的失效立即让门变红。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gate_baseline import load_baseline, split_violations, update_section  # noqa: E402

SOURCE_ROOTS = (
    "src/",
    "desktop/",
    "shared/",
    "crates/",
    "interfaces/",
    "plugins/",
    "scripts/",
    "qa/",
    "tests/",
    "docs/",
)

# 免检小节：历史（描述当时）与规划中（描述将来）都不要求当下存在。
# 中英文必须对称：英文页用 "History:" / "Planned:"，只豁免中文会让英文侧的
# 同一段历史叙述被误判成现状腐化。
EXEMPT_HEADING_RE = re.compile(
    r"历史|规划中|已废弃|历史记录"
    r"|Historical|History|Superseded|Deprecated|Planned|Planning|Retracted|Removed"
)

ROOT_FILES = (
    "Cargo.toml",
    "Cargo.lock",
    "justfile",
    "config.search.example.toml",
    "CHANGELOG.md",
    "AGENTS.md",
    "CLAUDE.md",
    "package.json",
    "pnpm-lock.yaml",
)

# 反引号内的 inline code：允许跨行？否，单行即可。
INLINE_CODE = re.compile(r"`([^`\n]+)`")

PLACEHOLDER = re.compile(r"[{}*<>$…]")

# 裸文件名检查：文档里写成 `foo.rs` / `foo.py` 的（没有目录前缀）也要能在仓库里
# 找到同名文件——这类引用不会被 SOURCE_ROOTS 路径检查抓到，但同样会随重构失效。
BARE_CODE_SUFFIXES = (".rs", ".py")
BARE_NAME_ALLOWLIST = {
    # Rust/Python 的通用文件名，任何仓库里都可能出现
    "mod.rs",
    "lib.rs",
    "main.rs",
    "build.rs",
    "setup.py",
    "conftest.py",
    "__init__.py",
}
# 建索引时跳过的目录（构建产物、体积大、非源码）
BARE_INDEX_SKIP_DIRS = {
    ".git",
    ".next",
    ".worktrees",
    "build",
    "node_modules",
    "target",
}


def build_basename_index(repo: Path) -> set[str]:
    """收集仓库里所有文件的 basename，用于裸文件名核对。"""
    names: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in BARE_INDEX_SKIP_DIRS]
        for name in filenames:
            names.add(name)
    return names


def is_bare_code_name(token: str) -> bool:
    return "/" not in token and token.endswith(BARE_CODE_SUFFIXES) and len(token) > 3


def normalize(token: str) -> str:
    """去掉行内修饰：句末标点、`::symbol`、`#anchor`、尾部斜杠。"""
    token = token.strip().strip("\"'`")
    token = token.rstrip(".,;:!?)】》")
    token = token.split("::", 1)[0]
    token = token.split("#", 1)[0]
    # 行号引用：src/foo.rs:335
    token = re.sub(r":\d+$", "", token)
    return token.strip()


def candidate_tokens(text: str):
    """从一行文本里提取所有待判定的路径 token。"""
    for match in INLINE_CODE.finditer(text):
        raw = match.group(1)
        # 一个 inline code 里可能有多个路径，用空白/逗号/顿号分开。
        for piece in re.split(r"[\s,，、]+", raw):
            token = normalize(piece)
            if not token:
                continue
            if token.startswith(SOURCE_ROOTS) or token in ROOT_FILES:
                yield token
            elif is_bare_code_name(token):
                yield token


def is_wildcard(token: str) -> bool:
    return bool(PLACEHOLDER.search(token))


def exempt_lines(text: str) -> list[bool]:
    """逐行标记该行是否落在「历史 / 规划中」小节里。"""
    exempt: list[bool] = []
    exempt_level: int | None = None
    for line in text.splitlines():
        heading = re.match(r"^(#+)\s", line)
        if heading:
            level = len(heading.group(1))
            if exempt_level is not None and level <= exempt_level:
                exempt_level = None
            if exempt_level is None and EXEMPT_HEADING_RE.search(line):
                exempt_level = level
            exempt.append(False)
            continue
        exempt.append(exempt_level is not None)
    return exempt


def check_token(token: str, repo: Path, docs_repo: Path, basename_index: set[str]):
    """返回 (状态, 说明)。状态 ∈ ok / missing / skipped。"""
    if is_wildcard(token):
        return "skipped", "含占位符"
    if is_bare_code_name(token):
        if token in BARE_NAME_ALLOWLIST:
            return "skipped", "通用文件名"
        if token in basename_index:
            return "ok", "basename"
        return "missing", "仓库内找不到同名文件"
    candidates = [repo]
    # 本仓库自有的脚本/文档（docs/ 优先指向 Aleph 仓，找不到再回落到文档仓）。
    if token.startswith(("scripts/", "docs/")):
        candidates.append(docs_repo)
    for base in candidates:
        target = base / token
        if token.endswith("/"):
            if target.is_dir():
                return "ok", str(base)
            continue
        if target.exists():
            return "ok", str(base)
    return "missing", ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Aleph 文档锚点门")
    parser.add_argument("--repo", default="../Aleph", help="Aleph 代码仓路径")
    parser.add_argument("--docs", default="content/docs", help="文档内容根（相对文档仓）")
    parser.add_argument("--docs-repo", default=".", help="文档仓自身路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--baseline", default=str(Path(__file__).resolve().parent / "baseline.json"))
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

    missing = []
    skipped = 0
    checked = 0
    basename_index = build_basename_index(repo)
    pages = sorted(content_root.rglob("*.mdx"))
    for page in pages:
        text = page.read_text(encoding="utf-8")
        flags = exempt_lines(text)
        for lineno, line in enumerate(text.splitlines(), start=1):
            if flags[lineno - 1]:
                continue
            for token in candidate_tokens(line):
                status, note = check_token(token, repo, docs_repo, basename_index)
                if status == "ok":
                    checked += 1
                elif status == "skipped":
                    skipped += 1
                else:
                    missing.append(
                        {
                            "file": str(page.relative_to(docs_repo)),
                            "line": lineno,
                            "token": token,
                            "kind": "bare" if is_bare_code_name(token) else "path",
                        }
                    )

    path_keys = [f"{m['file']}#{m['token']}" for m in missing if m["kind"] == "path"]
    bare_keys = [f"{m['file']}#{m['token']}" for m in missing if m["kind"] == "bare"]
    keys = path_keys + bare_keys
    baseline = load_baseline(Path(args.baseline))
    new_path, known_path = split_violations(path_keys, baseline.get("anchor", []))
    new_bare, known_bare = split_violations(bare_keys, baseline.get("bare_name", []))
    new_keys = new_path + new_bare
    known_keys = known_path + known_bare

    if args.update_baseline:
        fixed = update_section("anchor", path_keys, Path(args.baseline))
        fixed += update_section("bare_name", bare_keys, Path(args.baseline))
        print(
            f"基线已棘轮：anchor 段 {len(path_keys)} 条，bare_name 段 {len(bare_keys)} 条，"
            f"修掉 {len(fixed)} 条"
        )
        for item in fixed:
            print(f"  FIXED {item}")
        new_keys, known_keys = [], keys

    rel_missing = [
        f"{m['file']}:{m['line']}: {m['token']}" for m in missing
    ]
    new_set = set(new_keys)
    rel_new = [
        f"{m['file']}:{m['line']}: {m['token']}"
        for m in missing
        if f"{m['file']}#{m['token']}" in new_set
    ]
    if args.json:
        print(
            json.dumps(
                {
                    "pages": len(pages),
                    "checked": checked,
                    "skipped": skipped,
                    "missing": missing,
                    "new": new_keys,
                    "known": known_keys,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(
            f"页面 {len(pages)}，锚点 {checked + skipped}，失效 {len(missing)}"
            f"（路径 {len(path_keys)}，裸文件名 {len(bare_keys)}；"
            f"新增 {len(new_keys)}，基线旧债 {len(known_keys)}）"
        )
        for line in rel_new:
            print(f"NEW  {line}")
        if known_keys:
            print(f"（另有 {len(known_keys)} 条基线旧债，用 --update-baseline 棘轮）")

    return 1 if new_keys else 0


if __name__ == "__main__":
    sys.exit(main())
