#!/usr/bin/env python3
"""逐页列出 symbol_check 会检查的 token 及其判定，方便人工改写。

用法：
    python3 scripts/symbol_report.py --repo ../Aleph --page content/docs/zh/api/rust.mdx
    python3 scripts/symbol_report.py --repo ../Aleph --page content/docs/zh/api/rust.mdx --all

与 symbol_check.py 的判定完全一致（含代码块、含历史小节豁免），
差别只在于：它按页输出，并且给出每个 token 的行号。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from symbol_check import (  # noqa: E402
    CODE_RE,
    CRATE_ALIASES,
    CRATE_RE,
    JUST_RE,
    SYMBOL_ALLOWLIST,
    known_crates,
    known_just_targets,
    known_symbols,
    symbol_candidates,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="../Aleph")
    parser.add_argument("--page", required=True, help="页面路径（相对文档仓根）")
    parser.add_argument("--all", action="store_true", help="列出全部候选 token")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    page = Path(args.page)
    if not page.is_absolute():
        page = Path.cwd() / page

    symbols = known_symbols(repo)
    crates = known_crates(repo)
    just_targets = known_just_targets(repo)

    text = page.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    missing: dict[str, list[int]] = {}
    present: dict[str, list[int]] = {}

    for token, segments in symbol_candidates(text):
        if token in SYMBOL_ALLOWLIST:
            continue
        absent = [segment for segment in segments if segment not in symbols]
        bucket = missing if absent else present
        bucket.setdefault(token, [])
        for lineno, line in enumerate(lines, start=1):
            if f"`{token}`" in line:
                bucket[token].append(lineno)
                break

    print(f"== {page} ==")
    print(f"代码仓标识符 {len(symbols)}  crate {len(crates)}  just 目标 {len(just_targets)}")

    print(f"\n-- 符号不存在 ({len(missing)}) --")
    for token in sorted(missing):
        print(f"  {token}  行 {missing[token]}")
    if not missing:
        print("  无")

    # crate / just 目标
    crate_missing = []
    just_missing = []
    for span in CODE_RE.finditer(text):
        token = span.group(1).strip().rstrip(".,;:")
        if CRATE_RE.match(token) and token not in crates and token not in CRATE_ALIASES:
            crate_missing.append(token)
        for target in JUST_RE.findall(span.group(1)):
            if target not in just_targets:
                just_missing.append(target)
    if crate_missing:
        print(f"\n-- crate 不存在 ({len(crate_missing)}) --")
        for token in sorted(set(crate_missing)):
            print(f"  {token}")
    if just_missing:
        print(f"\n-- just 目标不存在 ({len(just_missing)}) --")
        for target in sorted(set(just_missing)):
            print(f"  just {target}")

    if args.all:
        print(f"\n-- 符号存在 ({len(present)}) --")
        for token in sorted(present):
            print(f"  {token}  行 {present[token]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
