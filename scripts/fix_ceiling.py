#!/usr/bin/env python3
"""Fix stale harness CEILING numbers and line references across the docs site.

Ground truth (Aleph repo):
  src/harness/tests/budget.rs:795 -> `const CEILING: usize = 5535;`
  src/harness/tests/budget.rs:313 -> the R10 "5 don'ts" #3 comment
  src/verification/tool_loop_verifier.rs -> ToolLoopVerifier (repeat_threshold)
There is no `TokenLoopVerifier` symbol in the tree.
"""

from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "content" / "docs"

REPLACEMENTS = [
    # current-tense statements
    (
        "- 当前 `CEILING` = **5055**（`src/harness/tests/budget.rs:335`，2026-07-26 修订）；不要把本节数字当副本",
        "- 当前 `CEILING` = **5535**（`src/harness/tests/budget.rs:795`）；不要把本节数字当副本",
    ),
    (
        "- Current `CEILING` = **5,055** (`src/harness/tests/budget.rs:335`, 2026-07-26 revision); treat any line count reproduced here as a stale copy",
        "- Current `CEILING` = **5,535** (`src/harness/tests/budget.rs:795`); treat any line count reproduced here as a stale copy",
    ),
    # historical sections: keep the 26.7.x number, point at the current constant too
    (
        "- 当时的 `CEILING` = **5055**（`src/harness/tests/budget.rs:335`，2026-07-26 修订）；不要把本节数字当副本",
        "- 当时的 `CEILING` = **5055**（26.7.x 期间）；当前值 **5535**（`src/harness/tests/budget.rs:795`）；不要把本节数字当副本",
    ),
    (
        "- At the time, `CEILING` = **5,055** (`src/harness/tests/budget.rs:335`, 2026-07-26 revision); treat any line count reproduced here as a stale copy",
        "- At the time, `CEILING` = **5,055** (during 26.7.x); the current value is **5,535** (`src/harness/tests/budget.rs:795`); treat any line count reproduced here as a stale copy",
    ),
    # api/rust.mdx
    (
        "行数总和压低于 `CEILING = 5,055`（`src/harness/tests/budget.rs:335`）",
        "行数总和压低于 `CEILING = 5,535`（`src/harness/tests/budget.rs:795`）",
    ),
    (
        "line totals held below `CEILING = 5,055` (`src/harness/tests/budget.rs:335`)",
        "line totals held below `CEILING = 5,535` (`src/harness/tests/budget.rs:795`)",
    ),
    # concepts/thinker.mdx
    (
        "`CEILING = 5055` 共享尺",
        "`CEILING = 5535` 共享尺",
    ),
    (
        "shared `CEILING = 5055` ruler",
        "shared `CEILING = 5535` ruler",
    ),
    # concepts/supervisor-verification.mdx: wrong symbol + wrong line
    ("`TokenLoopVerifier`（`repeat_threshold` = 5、连续同名同参数）",
     "`ToolLoopVerifier`（`repeat_threshold` = 5、连续同名同参数；`src/verification/tool_loop_verifier.rs`）"),
    ("`TokenLoopVerifier` (`repeat_threshold` = 5 consecutive identical tool calls)",
     "`ToolLoopVerifier` (`repeat_threshold` = 5 consecutive identical tool calls; `src/verification/tool_loop_verifier.rs`)"),
    ("`src/harness/tests/budget.rs:280` 写得很坦白",
     "`src/harness/tests/budget.rs:313` 写得很坦白"),
    ("`src/harness/tests/budget.rs:280` is blunt about why",
     "`src/harness/tests/budget.rs:313` is blunt about why"),
    ("ratchet 当前 **5055 行**（`src/harness/tests/budget.rs:335` 的 `CEILING`）",
     "ratchet 当前 **5535 行**（`src/harness/tests/budget.rs:795` 的 `CEILING`）"),
    ("The ratchet sits at **5,055 lines** today (`CEILING` in `src/harness/tests/budget.rs:335`)",
     "The ratchet sits at **5,535 lines** today (`CEILING` in `src/harness/tests/budget.rs:795`)"),
]


def main() -> int:
    changed = 0
    for path in sorted(DOCS.rglob("*.mdx")):
        text = original = path.read_text(encoding="utf-8")
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"updated {path.relative_to(DOCS.parent.parent)}")
    print(f"{changed} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
