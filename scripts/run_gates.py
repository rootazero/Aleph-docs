#!/usr/bin/env python3
"""Run the five documentation gates and print a summary table.

Gates:
  G1 anchor   — every source path the docs cite exists in the Aleph repo
  G1b method  — every dotted method/topic the docs cite exists in the code
  G2 facts    — no stale assertions, required semantics present
  G3 structure— navigation covers every page, no dead internal links
  G4 bilingual— zh and en have the same page set and heading skeleton
  G5 build    — next build + tsc + eslint (opt-in with --build; the build is
                slow and must not run while other writers hold .next)

Findings recorded in the baseline are accepted debt; only new findings fail.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS.parent


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def summarize(label: str, cmd: list[str]) -> tuple[str, str, int]:
    started = time.time()
    code, output = run(cmd)
    elapsed = time.time() - started
    if code == 0:
        state = "PASS"
    else:
        state = "FAIL"
    tail = "\n".join(output.strip().splitlines()[-12:])
    return label, f"{state} ({elapsed:.1f}s)", code if code != 0 else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Aleph 文档五道门")
    parser.add_argument("--repo", default="../Aleph")
    parser.add_argument("--docs", default="content/docs")
    parser.add_argument("--build", action="store_true", help="额外跑 G5 构建门（慢）")
    parser.add_argument("--update-baseline", action="store_true", help="把当前失效集合写回基线")
    args = parser.parse_args()

    common = ["--repo", args.repo, "--docs", args.docs]
    update = ["--update-baseline"] if args.update_baseline else []

    checks = [
        ("G1 锚点门", [sys.executable, str(SCRIPTS / "anchor_check.py"), *common, *update]),
        ("G1b 方法册", [sys.executable, str(SCRIPTS / "method_audit.py"), *common, *update]),
        ("G2 事实门", [sys.executable, str(SCRIPTS / "freshness_audit.py"), "--check", "facts", "--docs", args.docs, *update]),
        ("G3 结构门", [sys.executable, str(SCRIPTS / "freshness_audit.py"), "--check", "structure", "--docs", args.docs, *update]),
        ("G4 双语门", [sys.executable, str(SCRIPTS / "freshness_audit.py"), "--check", "bilingual", "--docs", args.docs, *update]),
    ]
    if args.build:
        checks.append(("G5 构建门", ["bash", "-lc", "pnpm exec next build && pnpm exec tsc --noEmit && pnpm exec eslint"]))

    print("== Aleph 文档门 ==")
    failed = 0
    for label, cmd in checks:
        name, state, code = summarize(label, cmd)
        print(f"{name:12s} {state}")
        failed += 1 if code else 0
    print("== 结果：{} ==".format("全部通过" if failed == 0 else f"{failed} 个门未通过"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
