#!/usr/bin/env python3
"""把符号门的结果按「改名 / 删除 / 外部名」分类，供第二轮对齐排期。

用法：python3 scripts/symbol_triage.py --repo ../Aleph --out /tmp/triage.json
"""
from __future__ import annotations

import argparse
import collections
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from symbol_check import (  # noqa: E402
    EXEMPT_HEADING_RE,
    known_crates,
    known_just_targets,
    known_symbols,
    symbol_candidates,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="../Aleph")
    ap.add_argument("--docs", default="content/docs")
    ap.add_argument("--docs-repo", default=".")
    ap.add_argument("--out", default="/tmp/triage.json")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    content_root = (Path(args.docs_repo).resolve() / args.docs).resolve()
    symbols = known_symbols(repo)
    crates = known_crates(repo) | known_just_targets(repo)  # 仅用于占位，避免未用告警
    del crates

    # 模糊匹配表：只对「文档里像 Rust/TS 标识符」的 token 做
    tokens = collections.Counter()
    pages = collections.defaultdict(list)
    for page in sorted(content_root.rglob("*.mdx")):
        rel = page.relative_to(content_root)
        text = page.read_text(encoding="utf-8", errors="ignore")
        for token, segments in symbol_candidates(text):
            missing = [s for s in segments if s not in symbols]
            if not missing:
                continue
            for seg in missing:
                tokens[seg] += 1
                pages[seg].append(str(rel))

    # 近似名：help 判断是「改名」还是「真删了」
    rename, gone = {}, {}
    for token in tokens:
        close = difflib.get_close_matches(token, sorted(symbols), n=3, cutoff=0.82)
        if close:
            rename[token] = close
        else:
            gone[token] = True

    result = {
        "rename": {k: v for k, v in rename.items()},
        "gone": {k: sorted(set(pages[k])) for k in gone},
        "counts": {"tokens": len(tokens), "rename": len(rename), "gone": len(gone)},
    }
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["counts"], ensure_ascii=False))
    for token, close in sorted(rename.items(), key=lambda kv: -tokens[kv[0]])[:60]:
        print(f"RENAME {token} ({tokens[token]}) -> {close}")
    print("---- gone ----")
    for token in sorted(gone, key=lambda t: -tokens[t])[:80]:
        print(f"GONE {token} ({tokens[token]}) pages={len(set(pages[token]))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
