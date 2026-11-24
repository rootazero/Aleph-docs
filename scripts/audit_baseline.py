#!/usr/bin/env python3
"""生成逐页判定基线 `docs/AUDIT-2026-11.md`。

判定来自两道门的机器信号（锚点门 + 事实/结构/双语门），是**基线**，
每个阶段执行时再按真实代码复核并修正判定词。

用法：
    python3 scripts/audit_baseline.py --repo ../Aleph [--out docs/AUDIT-2026-11.md]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# 阶段归属规则：按页面相对路径（相对 zh 根）匹配，先命中先算。
PHASE_RULES = [
    (r"^(architecture/(overview|1-2-3-4-model|desktop-bridge)|index\.mdx|philosophy/redlines|interfaces/webchat|development/|security/|gateway/auth)", "R1"),
    (r"^(gateway/protocol|api/jsonrpc|architecture/gateway)", "R2"),
    (r"^(concepts/(capability-system|extensions|extension-system|tool-infrastructure|builtin-tools|mcp-integration|plugins|marketplace))", "R3"),
    (r"^(concepts/(skills|skill-system|workflow|daemon|event-system|events)|architecture/(workflow|dispatcher|executor|proactive-dispatcher|cluster|teams|worldmodel|routing|orchestrator|harness))", "R4"),
    (r"^(terminology|changelog)", "R6"),
]

DEFAULT_PHASE = "R5"

VERDICT_ORDER = ["REWRITE", "UPDATE", "OK", "NEW"]

# 各阶段要新建的页面。
NEW_PAGES = [
    ("desktop-hosts/overview.mdx", "R1", "桌面宿主主线：NSH 架构、进程模型、Panel 挂载、Gateway 连接、生命周期"),
    ("desktop-hosts/panel.mdx", "R1", "Panel 宿主、模块化 Panel 与渲染点"),
    ("desktop-hosts/plugin-ui.mdx", "R1", "插件 UI 宿主侧契约（骨架，R4 填满）"),
    ("gateway/protocol-v1.mdx", "R2", "Protocol v1：帧、握手、事件信封、Snapshot/Replay、传输矩阵"),
    ("capabilities/capability-model.mdx", "R3", "Capability 描述符、kind/relation、Scope、Effect claim、Grant/Policy"),
    ("capabilities/slots-and-replacement.mdx", "R3", "槽位目录、三层模型、替换机制、解析顺序、回退语义"),
    ("capabilities/trust-and-backends.mdx", "R3", "后端与信任模型、WASM/进程插件、Hook 体系"),
    ("capabilities/hooks-and-prompts.mdx", "R3", "Hook 体系与 Prompt 分层替换、统一分发注册表"),
    ("capabilities/plugin-package.mdx", "R3", "包格式、发行版、生态兼容、可观测性"),
]


def phase_for(rel_path: str) -> str:
    for pattern, phase in PHASE_RULES:
        if re.search(pattern, rel_path):
            return phase
    return DEFAULT_PHASE


def run_json(script: str, args: list[str]) -> dict:
    result = subprocess.run(
        [sys.executable, script, *args, "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if not result.stdout.strip():
        return {}
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="生成逐页判定基线")
    parser.add_argument("--repo", default="../Aleph")
    parser.add_argument("--docs", default="content/docs")
    parser.add_argument("--docs-repo", default=".")
    parser.add_argument("--out", default="docs/AUDIT-2026-11.md")
    args = parser.parse_args()

    docs_repo = Path(args.docs_repo).resolve()
    scripts = docs_repo / "scripts"

    anchors = run_json(str(scripts / "anchor_check.py"), ["--repo", args.repo, "--docs", args.docs])
    facts = run_json(str(scripts / "freshness_audit.py"), ["--check", "all", "--docs", args.docs])

    anchor_by_page: dict[str, list[str]] = defaultdict(list)
    for item in anchors.get("missing", []):
        anchor_by_page[item["file"]].append(item["token"])

    stale_by_page: dict[str, list[str]] = defaultdict(list)
    deadlink_by_page: dict[str, list[str]] = defaultdict(list)
    bilingual_by_page: dict[str, list[str]] = defaultdict(list)
    for name in ("facts", "structure", "bilingual"):
        for item in facts.get(name, []):
            file_name = item.get("file", "")
            if name == "facts":
                stale_by_page[file_name].append(item.get("reason", ""))
            elif item.get("kind") == "dead-link":
                deadlink_by_page[file_name].append(item.get("reason", ""))
            elif name == "bilingual":
                bilingual_by_page[file_name].append(item.get("reason", ""))

    zh_root = docs_repo / args.docs / "zh"
    pages = sorted(
        str(p.relative_to(zh_root)).replace("\\", "/") for p in zh_root.rglob("*.mdx")
    )

    rows = []
    for page in pages:
        key_zh = f"zh/{page}"
        key_en = f"en/{page}"
        broken = anchor_by_page.get(key_zh, []) + anchor_by_page.get(key_en, [])
        stale = stale_by_page.get(key_zh, []) + stale_by_page.get(key_en, [])
        dead = deadlink_by_page.get(key_zh, []) + deadlink_by_page.get(key_en, [])
        mismatch = bilingual_by_page.get(page, [])

        if stale:
            verdict = "REWRITE"
        elif broken or dead or mismatch:
            verdict = "UPDATE"
        else:
            verdict = "OK"

        reasons = []
        if stale:
            reasons.append(f"现状表述过期 ×{len(stale)}")
        if broken:
            reasons.append("失效锚点 " + "、".join(sorted(set(broken))[:6]))
        if dead:
            reasons.append("站内死链 ×" + str(len(dead)))
        if mismatch:
            reasons.append("双语标题骨架不一致")

        rows.append(
            {
                "page": page,
                "verdict": verdict,
                "reason": "；".join(reasons) if reasons else "无机器信号，需人工复核",
                "phase": phase_for(page),
            }
        )

    counts = defaultdict(int)
    for row in rows:
        counts[row["verdict"]] += 1

    out_path = docs_repo / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        handle.write("# Aleph 文档逐页判定（2026-11 基线）\n\n")
        handle.write(
            "> 本表由 `scripts/audit_baseline.py` 从两道门的机器信号生成，**是基线不是终稿**。\n"
            "> 每个阶段执行时按真实代码复核该阶段的页面，修正判定词与理由，并把阶段结论补进\n"
            "> `docs/VERIFICATION-2026-11.md`。\n\n"
        )
        handle.write("## 判定词表\n\n")
        handle.write(
            "| 判定 | 含义 |\n|---|---|\n"
            "| REWRITE | 核心框架已过时（现状表述与代码冲突），需重写 |\n"
            "| UPDATE | 框架仍成立，但锚点/链接/细节需要按现状更新 |\n"
            "| OK | 机器信号干净，仍需人工抽查 |\n"
            "| NEW | 本轮要新建的页面 |\n\n"
        )
        handle.write("## 汇总\n\n")
        handle.write(f"- zh 页面总数：**{len(rows)}**（en 镜像同数）\n")
        for verdict in VERDICT_ORDER:
            if verdict in counts:
                handle.write(f"- {verdict}：{counts[verdict]}\n")
        handle.write("\n## 待新建页面\n\n")
        handle.write("| 页面 | 阶段 | 目标 |\n|---|---|---|\n")
        for path, phase, goal in NEW_PAGES:
            handle.write(f"| `{path}` | {phase} | {goal} |\n")
        handle.write("\n## 逐页判定\n\n")
        handle.write("| 页面 | 判定 | 理由 | 阶段 |\n|---|---|---|---|\n")
        for row in rows:
            reason = row["reason"].replace("|", "/")
            handle.write(
                f"| `{row['page']}` | {row['verdict']} | {reason} | {row['phase']} |\n"
            )

    print(f"已写出 {out_path}")
    print("判定分布：" + "，".join(f"{k} {counts[k]}" for k in VERDICT_ORDER if k in counts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
