#!/usr/bin/env python3
"""按文件分组生成 R5「方法册」修复简报。

输入：
  - method_audit.py 的 JSON 输出（ghost 位置 + missing 方法名）
  - /tmp/r5/method_resolution.md（逐条判定与候选替换）

输出：/tmp/r5/method_briefs/<group>.md，每个简报列出该组文件的
      幽灵方法 → 处置建议、缺失方法 → 应补写的位置。
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path("/home/zou/data/workspace/Aleph-docs")
OUT = Path("/tmp/r5/method_briefs")

# 在飞 worker 正在改的文件，本轮不派，避免写冲突。
BUSY = {
    # wave8 arch
    "architecture/clawhub.mdx", "architecture/design-patterns.mdx", "architecture/dispatcher.mdx",
    "architecture/executor.mdx", "architecture/harness.mdx", "architecture/memory.mdx",
    "architecture/overview.mdx", "architecture/proactive-dispatcher.mdx", "architecture/providers.mdx",
    "architecture/resilience.mdx", "architecture/routing.mdx", "architecture/sandbox.mdx",
    "architecture/session-service.mdx", "architecture/sessions.mdx", "architecture/thinker.mdx",
    "architecture/tools.mdx", "architecture/worldmodel.mdx",
    # wave7 conceptsA / conceptsB
    "concepts/agent-components.mdx", "concepts/agent-runtime.mdx", "concepts/ai-providers.mdx",
    "concepts/artifacts-deliverables.mdx", "concepts/clawhub.mdx", "concepts/core-types.mdx",
    "concepts/event-system.mdx", "concepts/extensions.mdx", "concepts/extension-system.mdx",
    "concepts/gateway.mdx", "concepts/generation.mdx", "concepts/looping-goal-strategy.mdx",
    "concepts/markdown-utils.mdx", "concepts/media-processing.mdx", "concepts/memory.mdx",
    "concepts/resilience.mdx", "concepts/secret-management.mdx", "concepts/security-primitives.mdx",
    "concepts/task-scheduling.mdx", "concepts/thinker.mdx", "concepts/tool-infrastructure.mdx",
    "concepts/voice-streaming.mdx", "concepts/workspaces.mdx",
    # wave8 gatewayd
    "gateway/auth.mdx", "gateway/methods/arena.mdx", "gateway/methods/channels.mdx",
    "gateway/methods/chat.mdx", "gateway/methods/extensions.mdx", "gateway/methods/group_chat.mdx",
    "gateway/methods/heartbeat.mdx", "gateway/methods/memory.mdx", "gateway/methods/plugins.mdx",
    "gateway/methods/providers.mdx", "gateway/methods/services.mdx", "gateway/methods/teams.mdx",
    "gateway/methods/wizard.mdx", "gateway/methods/workspace.mdx",
    # wave7 rest
    "changelog.mdx", "development/contributing.mdx", "philosophy/agent-thinking.mdx",
    "philosophy/domain-modeling.mdx", "security/exec-approval.mdx", "security/ipc.mdx",
    "security/overview.mdx", "security/sandboxing.mdx", "terminology.mdx", "tools/overview.mdx",
    # wave9 r3-b / r3-c
    "capabilities/slots-and-replacement.mdx", "capabilities/trust-and-backends.mdx",
    "capabilities/hooks-and-prompts.mdx", "capabilities/plugin-package.mdx",
    # wave10 r4-b
    "interfaces/webchat.mdx",
}

# 分组：按顶层目录 + 人工拆分，保证每组不超过 25 个文件。
GROUP_RULES = [
    ("gateway-methods", lambda p: p.startswith("gateway/methods/")),
    ("gateway-root", lambda p: p.startswith("gateway/")),
    ("architecture", lambda p: p.startswith("architecture/")),
    ("concepts", lambda p: p.startswith("concepts/")),
    ("security-cli", lambda p: p.startswith(("security/", "cli/", "interfaces/", "automation/"))),
    ("other", lambda p: True),
]


def load_resolution() -> dict[str, dict]:
    """方法名 → 判定行（ghost 表）。"""
    out: dict[str, dict] = {}
    path = Path("/tmp/r5/method_resolution.md")
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 5:
            continue
        name = cols[0].strip("`")
        if "." not in name:
            continue
        out.setdefault(name, {"verdict": cols[1], "candidate": cols[2], "evidence": cols[3], "action": cols[4]})
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    raw = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "method_audit.py"), "--repo", "../Aleph", "--json"],
        cwd=REPO, capture_output=True, text=True,
    )
    data = json.loads(raw.stdout)
    resolution = load_resolution()

    per_file: dict[str, set[str]] = defaultdict(set)
    for method, locations in data["ghost_locations"].items():
        for loc in locations:
            per_file[loc].add(method)

    # 缺哪些方法、应该补到哪个分册：由 missing 名字的前缀推。
    missing_prefix: dict[str, list[str]] = defaultdict(list)
    for m in data["known_missing"] + data["new_missing"]:
        missing_prefix[m.split(".")[0]].append(m)

    groups: dict[str, list[str]] = defaultdict(list)
    for path in sorted(per_file):
        rel = path.split("content/docs/", 1)[1]
        rel = re.sub(r"^(zh|en)/", "", rel)
        if rel in BUSY:
            continue
        for name, test in GROUP_RULES:
            if test(rel):
                groups[name].append(path)
                break

    for name, files in sorted(groups.items()):
        lines = [
            f"# 方法册修复简报 · {name}",
            "",
            "你是 Aleph 文档站的**方法册校对员**。下面每个文件里都出现了在代码里",
            "**不存在**的方法名（ghost）。你的任务：按判定表把它们改成真实的方法名，",
            "或者在无法确认时**删掉**该方法表述，绝不保留假方法名。",
            "",
            "## 判定表怎么读",
            "",
            "| 列 | 含义 |",
            "|----|------|",
            "| 判定 | G-1 = 方法在代码里完全不存在；G-2 = 只有形近的真实方法 |",
            "| 候选 | 代码里形近的真实方法名 |",
            "| 证据 | 候选在源码中的位置 |",
            "| 处置 | 该怎么改 |",
            "",
            "**处置优先级**：",
            "",
            "1. 判定给了**候选**且证据明确 → 把文档里的方法名改成候选（核对候选的语义与原文是否一致；",
            "   语义不一致就不要换，删掉该方法表述）。",
            "2. 判定是「未找到」→ 文档里的方法名是**假的**：删掉整行/整句；若原文在讲一个真实概念，",
            "   改写成那个概念在本仓库的真实名字（用 grep 找到它）。",
            "3. 任何情况下都不能写出代码里不存在的 `a.b` 方法名。",
            "",
            "## 硬性规则",
            "",
            "- 只改本简报列出的文件，不碰 `meta.json`，不碰别的页面。",
            "- zh 与 en 必须同步改，标题骨架保持一致。",
            "- 改完不要新增代码里没有的反引号 `a.b` 标识符。",
            "- 不运行 pnpm build / next build；不 git commit / push。",
            "",
        ]
        for path in files:
            lines.append(f"## {path}")
            lines.append("")
            for method in sorted(per_file[path]):
                info = resolution.get(method)
                if info:
                    lines.append(
                        f"- `{method}` — 判定：{info['verdict']}；候选：{info['candidate']}；"
                        f"证据：{info['evidence']}；处置：{info['action']}"
                    )
                else:
                    lines.append(
                        f"- `{method}` — 判定表里没有这一条（判定表生成后页面又变了）。"
                        f"请自己 grep `../Aleph` 确认它是否存在：不存在就删掉或改成真实名字。"
                    )
            lines.append("")
        # 该组涉及的 missing 方法，提示补写。
        rels = [p.split("content/docs/", 1)[1] for p in files]
        need = sorted({m for m in data["known_missing"] + data["new_missing"]
                       if any(r.split("content/docs/")[-1].split("/")[0] in m for r in rels)})
        if need:
            lines.append("## 本组可能需要补写的方法")
            lines.append("")
            lines.append("以下方法**在代码里已注册但文档站完全没提**。如果本组文件是该方法的自然归属，")
            lines.append("就补一个条目（带 `src/gateway/method_census.rs` 的锚点）；如果不属于本组，忽略。")
            lines.append("")
            for m in need:
                lines.append(f"- `{m}`")
            lines.append("")
        (OUT / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")
        # 同一批页面的相对路径列表（相对 content/docs），供 --files-from 使用。
        rel_paths = sorted({re.sub(r"^content/docs/(zh|en)/", "", p) for p in files})
        (OUT / f"{name}.files.txt").write_text("\n".join(rel_paths) + "\n", encoding="utf-8")
        print(f"{name}: {len(files)} 个文件")

    skipped = sorted({p for p in per_file if re.sub(r"^content/docs/(zh|en)/", "", p) in BUSY})
    print(f"跳过（在飞 worker 负责）: {len(skipped)} 个文件")
    print(f"输出目录: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
