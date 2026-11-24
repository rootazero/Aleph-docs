#!/usr/bin/env python3
"""生成终验报告的机器部分：`docs/VERIFICATION-2026-11.md`。

报告分两部分：
- 机器部分（本脚本生成）：五道门的结果、各门失效条数、页面与锚点规模。
- 人工部分（主 agent 写）：逐阶段结论、真值分层说明、遗留债务与复核方法。

脚本只读取门禁脚本的输出，不修改文档站内容。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS.parent


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def count_pages(docs: str) -> tuple[int, int]:
    root = REPO_ROOT / docs
    zh = len(list((root / "zh").rglob("*.mdx")))
    en = len(list((root / "en").rglob("*.mdx")))
    return zh, en


def first_int(pattern: str, text: str) -> int:
    m = re.search(pattern, text)
    return int(m.group(1)) if m else -1


def main() -> int:
    parser = argparse.ArgumentParser(description="生成终验报告的机器部分")
    parser.add_argument("--repo", default="../Aleph")
    parser.add_argument("--docs", default="content/docs")
    parser.add_argument("--out", default="docs/VERIFICATION-2026-11.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    common = ["--repo", args.repo, "--docs", args.docs]
    gates: list[tuple[str, str, int, str]] = []

    for label, script, extra in [
        ("G1 锚点门", "anchor_check.py", []),
        ("G1b 方法册", "method_audit.py", []),
        ("G2 事实门", "freshness_audit.py", ["--check", "facts"]),
        ("G3 结构门", "freshness_audit.py", ["--check", "structure"]),
        ("G4 双语门", "freshness_audit.py", ["--check", "bilingual"]),
    ]:
        # freshness_audit 不认 --repo（它只读文档站），所以按脚本分派参数。
        args_for_script = common if script != "freshness_audit.py" else ["--docs", args.docs]
        code, out = run([sys.executable, str(SCRIPTS / script), *args_for_script, *extra])
        gates.append((label, "PASS" if code == 0 else "FAIL", code, out))

    zh, en = count_pages(args.docs)
    anchor_out = gates[0][3]
    checked = first_int(r"锚点\s+(\d+)", anchor_out)
    failed = first_int(r"失效\s+(\d+)", anchor_out)

    summary = {
        "gates": [
            {"name": name, "state": state, "exit_code": code}
            for name, state, code, _ in gates
        ],
        "pages": {"zh": zh, "en": en},
        "anchors_checked": checked,
        "anchors_failed": failed,
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if all(g["state"] == "PASS" for g in summary["gates"]) else 1

    rows = []
    for name, state, code, out in gates:
        detail_lines = []
        for line in out.splitlines():
            line = line.strip()
            if not line or line.startswith("==") or line.startswith("已写入"):
                continue
            detail_lines.append(line)
            if len(detail_lines) >= 3:
                break
        detail = "<br>".join(detail_lines).replace("|", "\\|")
        rows.append(f"| {name} | {state} | {detail} |")

    body = f"""# Aleph 文档站终验报告（2026-11）

> 本文件由 `scripts/verification_report.py` 生成**机器部分**，逐阶段结论由主 agent 撰写。
> 复核命令：`python3 scripts/run_gates.py --repo ../Aleph --build`。

## 门禁结果

| 门 | 结果 | 明细 |
|----|------|------|
{chr(10).join(rows)}

## 规模

- 页面：zh {zh} 页 / en {en} 页
- 代码锚点：{checked} 个被检查，{failed} 个失效

## 逐阶段结论

（待填）
"""
    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # 人工部分写在标记之间，脚本重跑时保留它。
    manual = ""
    if out_path.exists():
        existing = out_path.read_text(encoding="utf-8")
        if "<!-- MANUAL:BEGIN -->" in existing and "<!-- MANUAL:END -->" in existing:
            manual = existing.split("<!-- MANUAL:BEGIN -->", 1)[1].split("<!-- MANUAL:END -->", 1)[0]
    if not manual:
        manual = "\n（待填）\n"
    body = body.replace("## 逐阶段结论\n\n（待填）\n", f"## 逐阶段结论\n\n<!-- MANUAL:BEGIN -->{manual}<!-- MANUAL:END -->\n")
    out_path.write_text(body, encoding="utf-8")
    print(f"已写入 {out_path}")
    return 0 if all(g["state"] == "PASS" for g in summary["gates"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
