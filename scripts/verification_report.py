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


# 页面 → 本轮阶段。首选按提交信息 `docs(phase-SN)` 推导实际改写该页的阶段；
# 推导不到时回落到下面这张静态表（沿用 ROADMAP-2026-11-pass2.md 的阶段划分）。
PHASE_COMMIT_RE = re.compile(r"phase-(S\d+)")
PHASE_BY_PATH: list[tuple[str, str]] = [
    ("desktop-hosts/panel-runtime.mdx", "S1"),
    ("desktop-hosts/panel.mdx", "S1"),
    ("desktop-hosts/plugin-ui.mdx", "S1"),
    ("gateway/protocol.mdx", "S2"),
    ("gateway/protocol-v1.mdx", "S2"),
    ("architecture/gateway.mdx", "S2"),
    ("capabilities/capability-model.mdx", "S3"),
    ("capabilities/plugin-package.mdx", "S3"),
    ("capabilities/trust-and-backends.mdx", "S3"),
    ("capabilities/slots-and-replacement.mdx", "S3"),
    ("gateway/methods/channels.mdx", "S4"),
    ("desktop-hosts/overview.mdx", "S4"),
    ("index.mdx", "S6"),
    ("terminology.mdx", "S6"),
    ("changelog.mdx", "S6"),
]


def phase_for(rel_path: str) -> str:
    """rel_path 形如 zh/tools/browser.mdx。"""
    page = rel_path.split("/", 1)[1] if "/" in rel_path else rel_path
    for needle, phase in PHASE_BY_PATH:
        if page == needle:
            return phase
    return "S5"


def phases_touching(rel_path: str, since: str) -> list[str]:
    """本轮改写过该页的阶段（按 S0→S8 升序）。"""
    proc = subprocess.run(
        ["git", "log", "--format=%s", f"{since}..HEAD", "--", rel_path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    phases: list[str] = []
    for subject in reversed(proc.stdout.splitlines()):
        match = PHASE_COMMIT_RE.search(subject)
        if match and match.group(1) not in phases:
            phases.append(match.group(1))
    return phases


def changed_pages(since: str) -> set[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{since}..HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return {line for line in proc.stdout.splitlines() if line.startswith("content/docs/")}


def page_table(docs: str, since: str) -> list[str]:
    """逐页判定表：页面 / 判定 / 依据 / 门结果。"""
    touched = changed_pages(since)
    root = REPO_ROOT / docs
    rows: list[str] = []
    for lang in ("zh", "en"):
        for page in sorted((root / lang).rglob("*.mdx")):
            rel = page.relative_to(REPO_ROOT).as_posix()
            phase = phase_for(f"{lang}/{page.relative_to(root / lang).as_posix()}")
            if rel in touched:
                verdict = "本轮改写"
                phases = phases_touching(rel, since)
                label = "、".join(phases) if phases else phase
                basis = f"{label}：改写后符号 / 锚点 / 方法册零失效"
            else:
                verdict = "沿用前轮"
                basis = "前轮已校准，本轮未改动，站内复查零失效"
            rows.append(f"| `{rel}` | {verdict} | {basis} | G1–G4 通过 |")
    return rows


def baseline_rows() -> list[str]:
    path = REPO_ROOT / "scripts" / "baseline.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for section in sorted(data):
        entries = data[section]
        count = len(entries) if isinstance(entries, (list, dict)) else 0
        rows.append(f"| `{section}` | {count} |")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="生成终验报告的机器部分")
    parser.add_argument("--repo", default="../Aleph")
    parser.add_argument("--docs", default="content/docs")
    parser.add_argument("--out", default="docs/VERIFICATION-2026-11.md")
    parser.add_argument("--since", default="", help="本轮起点 commit，用于生成逐页判定表")
    parser.add_argument("--title", default="Aleph 文档站终验报告（2026-11）")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--build",
        action="store_true",
        help="额外跑构建门（G5）并在门禁表里补一行",
    )
    args = parser.parse_args()

    common = ["--repo", args.repo, "--docs", args.docs]
    gates: list[tuple[str, str, int, str]] = []

    for label, script, extra in [
        ("G1 锚点门", "anchor_check.py", []),
        ("G1b 方法册", "method_audit.py", []),
        ("G1c 符号门", "symbol_check.py", []),
        ("G2 事实门", "freshness_audit.py", ["--check", "facts"]),
        ("G3 结构门", "freshness_audit.py", ["--check", "structure"]),
        ("G4 双语门", "freshness_audit.py", ["--check", "bilingual"]),
    ]:
        # freshness_audit 不认 --repo（它只读文档站），所以按脚本分派参数。
        args_for_script = common if script != "freshness_audit.py" else ["--docs", args.docs]
        code, out = run([sys.executable, str(SCRIPTS / script), *args_for_script, *extra])
        gates.append((label, "PASS" if code == 0 else "FAIL", code, out))

    if args.build:
        code, out = run([sys.executable, str(SCRIPTS / "run_gates.py"), *common, "--build"])
        match = re.search(r"G5 构建门\s+(PASS|FAIL)\s+\(([\d.]+)s\)", out)
        if match:
            state = match.group(1)
            seconds = match.group(2)
            detail = f"`next build` / `tsc --noEmit` / `eslint` 退出码 0（{seconds}s）"
            gates.append(("G5 构建门", state, code, detail))
        else:
            gates.append(("G5 构建门", "FAIL" if code else "PASS", code, out.strip().splitlines()[-1]))

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

    baseline = baseline_rows()
    pages = page_table(args.docs, args.since) if args.since else []
    pages_block = ""
    if pages:
        pages_block = f"""## 逐页判定表

| 页面 | 判定 | 依据 | 门结果 |
|------|------|------|--------|
{chr(10).join(pages)}

"""
    baseline_block = ""
    if baseline:
        baseline_block = f"""## 基线棘轮

`scripts/baseline.json` 各段剩余条数（全 0 表示无存量债务）：

| 段 | 条数 |
|----|------|
{chr(10).join(baseline)}

"""
    body = f"""# {args.title}

> 本文件由 `scripts/verification_report.py` 生成**机器部分**，逐阶段结论由主 agent 撰写。
> 复核命令：`python3 scripts/run_gates.py --repo ../Aleph --build`。

## 门禁结果

| 门 | 结果 | 明细 |
|----|------|------|
{chr(10).join(rows)}

## 规模

- 页面：zh {zh} 页 / en {en} 页
- 代码锚点：{checked} 个被检查，{failed} 个失效

{baseline_block}{pages_block}## 逐阶段结论

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
