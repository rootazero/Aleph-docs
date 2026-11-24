#!/usr/bin/env python3
"""事实门 / 结构门 / 双语门（G2 / G3 / G4）。

用法：
    python3 scripts/freshness_audit.py --check all --repo ../Aleph
    python3 scripts/freshness_audit.py --check facts
    python3 scripts/freshness_audit.py --check structure --json

子检查：
  facts      过期断言黑名单 + 指定页面的必备语义标记
  structure  meta.json 收录完整性、孤儿页面、站内相对链接可解析
  bilingual  zh/en 页面集合一致 + 同名页面 `##` 标题骨架一致

退出码：0 = 通过；1 = 有失败项；2 = 参数/环境错误。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gate_baseline import load_baseline, split_violations, update_section  # noqa: E402

LANGS = ("zh", "en")

# ── facts ────────────────────────────────────────────────────────────────────

# 过期断言：(正则, 说明)。命中即失败，除非该行位于「历史」小节内。
#
# 注：`aleph-bridge`（Swift 助手进程）**不是**过期模型——它仍是 macOS PIM 等原生
# 能力的现行实现（`desktop/macos/src/pim.rs` 的 `MacOSPim` 走 `SwiftBridge`），
# 见 `docs/reference/DESKTOP_BRIDGE.md`。故不列入过期模式。
STALE_PATTERNS = [
    (
        re.compile(r"Tauri", re.IGNORECASE),
        "Tauri 出现在现状描述里（桌面宿主主线已改为 NSH，Tauri 为待删除的过渡期遗留）",
    ),
    (
        re.compile(r"CapabilityDeclaration"),
        "旧的 CapabilityDeclaration 声明枚举（现行能力模型在 src/capability/）",
    ),
]

# 页面级豁免：页面若已指向现行能力子系统，它谈 CapabilityDeclaration 时是在讲
# 「插件声明模型 vs 运行时能力模型」的分工，而不是把旧枚举当成现行能力模型。
CAPABILITY_PAGE_MARKERS = (
    "src/capability/",
    "aleph-slot-api",
    "capability-model",
    "capabilities/capability-model",
)

# 允许出现上述词汇的行内豁免词（说明这行在讲历史/退场）。
EXEMPT_WORDS = (
    "历史",
    "History",
    "过渡",
    "遗留",
    "退场",
    "将删除",
    "已删除",
    "待删除",
    "legacy",
    "Legacy",
    "deprecated",
    "removed",
    "removal",
)

# 对照语境豁免：同一行把旧模型与现行模型**对比**时，它是在解释迁移，
# 而不是把旧模型当成现状。这类行不构成过期断言。
COMPARISON_WORDS = (
    "旧模型",
    "old model",
    "新模型",
    "new model",
    "对照",
    "comparison",
    "取代",
    "superseded",
    "rather than",
)

# 页面 → 必须出现的语义标记。页面不存在时不报（由 structure 门负责）。
REQUIRED_MARKERS = {
    "desktop-hosts/overview.mdx": ["desktop/nsh-shell", "system.hello"],
    "desktop-hosts/panel.mdx": ["interfaces/webchat"],
    "gateway/protocol-v1.mdx": ["shared/protocol/src/framing.rs", "system.hello"],
    "capabilities/capability-model.mdx": ["src/capability/"],
    "capabilities/slots-and-replacement.mdx": ["crates/aleph-slot-api"],
}

HISTORY_HEADING = re.compile(r"^##\s.*(历史|History|旧|Legacy)")

# 整页豁免：变更日志逐条记录的是已发布的历史行为，按定义就是「历史」。
EXEMPT_FILES = {"changelog.mdx"}

# ── structure ────────────────────────────────────────────────────────────────

MDX_LINK = re.compile(r"\]\((\.{1,2}/[^)\s#]*)(#[^)]*)?\)")


def history_lines(text: str) -> set[int]:
    """返回「历史」小节覆盖的行号集合。"""
    lines = text.splitlines()
    inside = False
    covered = set()
    for idx, line in enumerate(lines, start=1):
        if line.startswith("## "):
            inside = bool(HISTORY_HEADING.match(line))
        if inside:
            covered.add(idx)
    return covered


def check_facts(content_root: Path):
    findings = []
    for lang in LANGS:
        lang_root = content_root / lang
        if not lang_root.is_dir():
            continue
        for page in sorted(lang_root.rglob("*.mdx")):
            rel = page.relative_to(content_root / lang)
            text = page.read_text(encoding="utf-8")
            covered = history_lines(text)
            if page.name in EXEMPT_FILES:
                covered = set(range(1, len(text.splitlines()) + 1))
            # 页面级豁免：已指向现行能力子系统的页面不算「拿旧枚举当现状」。
            capability_aware = any(
                marker in text for marker in CAPABILITY_PAGE_MARKERS
            )
            for lineno, line in enumerate(text.splitlines(), start=1):
                if lineno in covered:
                    continue
                if any(word in line for word in EXEMPT_WORDS):
                    continue
                if any(word in line for word in COMPARISON_WORDS):
                    continue
                for pattern, reason in STALE_PATTERNS:
                    if not pattern.search(line):
                        continue
                    if (
                        capability_aware
                        and "CapabilityDeclaration" in pattern.pattern
                    ):
                        break
                    findings.append(
                        {
                            "kind": "stale",
                            "file": f"{lang}/{rel}",
                            "line": lineno,
                            "reason": reason,
                            "text": line.strip()[:160],
                        }
                    )
                    break
            markers = REQUIRED_MARKERS.get(str(rel))
            if markers:
                for marker in markers:
                    if marker not in text:
                        findings.append(
                            {
                                "kind": "missing-marker",
                                "file": f"{lang}/{rel}",
                                "line": 0,
                                "reason": f"缺少必备语义标记：{marker}",
                                "text": "",
                            }
                        )
    return findings


def read_meta(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"__error__": str(exc)}


def collect_meta_pages(lang_root: Path):
    """从根 meta.json 递归展开，列出所有被收录的页面与目录。"""
    reachable_mdx = set()
    reachable_dirs = set()
    problems = []
    stack = [lang_root]
    seen = set()
    while stack:
        directory = stack.pop()
        if directory in seen:
            continue
        seen.add(directory)
        meta_path = directory / "meta.json"
        if not meta_path.exists():
            continue
        meta = read_meta(meta_path)
        if "__error__" in meta:
            problems.append(f"{meta_path}: meta.json 解析失败：{meta['__error__']}")
            continue
        for entry in meta.get("pages", []):
            if entry == "---":
                continue
            target = directory / entry
            if target.is_dir():
                if not (target / "meta.json").exists():
                    problems.append(f"{target.relative_to(lang_root)}: 目录缺 meta.json")
                reachable_dirs.add(target)
                stack.append(target)
            elif target.with_suffix(".mdx").exists():
                reachable_mdx.add(target.with_suffix(".mdx"))
            else:
                problems.append(
                    f"{(target).relative_to(lang_root)}: meta.json 列出但文件不存在"
                )
    return reachable_mdx, reachable_dirs, problems


def check_structure(content_root: Path):
    findings = []
    for lang in LANGS:
        lang_root = content_root / lang
        if not lang_root.is_dir():
            findings.append({"kind": "structure", "file": lang, "reason": "语言目录缺失"})
            continue
        reachable, _, problems = collect_meta_pages(lang_root)
        for problem in problems:
            findings.append({"kind": "structure", "file": f"{lang}", "reason": problem})
        on_disk = set(lang_root.rglob("*.mdx"))
        # 语言首页由框架直接提供，不需要出现在 meta.json 里。
        on_disk = {p for p in on_disk if p.name != "index.mdx"}
        for orphan in sorted(on_disk - reachable):
            findings.append(
                {
                    "kind": "orphan",
                    "file": f"{lang}/{orphan.relative_to(lang_root)}",
                    "reason": "页面未被任何 meta.json 收录",
                }
            )
        for page in sorted(on_disk):
            text = page.read_text(encoding="utf-8")
            for lineno, line in enumerate(text.splitlines(), start=1):
                for match in MDX_LINK.finditer(line):
                    raw_target = match.group(1)
                    target = (page.parent / raw_target).resolve()
                    # 指到文档内容根之外的链接（例如代码仓内的相对路径）不归本站管。
                    try:
                        target.relative_to(content_root)
                    except ValueError:
                        continue
                    candidates = [target]
                    if not target.suffix:
                        candidates.append(target.with_suffix(".mdx"))
                    if not any(c.exists() for c in candidates):
                        findings.append(
                            {
                                "kind": "dead-link",
                                "file": f"{lang}/{page.relative_to(lang_root)}",
                                "line": lineno,
                                "reason": f"站内链接不可解析：{match.group(1)}",
                            }
                        )
    return findings


def heading_skeleton(text: str):
    """返回 `##` / `###` 的层级序列（不含标题文本，zh/en 文本不同）。"""
    levels = []
    for line in text.splitlines():
        match = re.match(r"^(#{2,4})\s+\S", line)
        if match:
            levels.append(len(match.group(1)))
    return levels


def check_bilingual(content_root: Path):
    findings = []
    roots = {lang: content_root / lang for lang in LANGS}
    if not all(root.is_dir() for root in roots.values()):
        return [{"kind": "bilingual", "file": "-", "reason": "zh/en 目录不齐"}]
    zh_files = {
        str(p.relative_to(roots["zh"])).replace("\\", "/") for p in roots["zh"].rglob("*.mdx")
    }
    en_files = {
        str(p.relative_to(roots["en"])).replace("\\", "/") for p in roots["en"].rglob("*.mdx")
    }
    for missing in sorted(zh_files - en_files):
        findings.append(
            {"kind": "bilingual", "file": f"zh/{missing}", "reason": "缺少英文镜像页"}
        )
    for missing in sorted(en_files - zh_files):
        findings.append(
            {"kind": "bilingual", "file": f"en/{missing}", "reason": "缺少中文镜像页"}
        )
    for shared_path in sorted(zh_files & en_files):
        zh_text = (roots["zh"] / shared_path).read_text(encoding="utf-8")
        en_text = (roots["en"] / shared_path).read_text(encoding="utf-8")
        zh_levels = heading_skeleton(zh_text)
        en_levels = heading_skeleton(en_text)
        if zh_levels != en_levels:
            findings.append(
                {
                    "kind": "bilingual",
                    "file": shared_path,
                    "reason": f"标题骨架不一致：zh {len(zh_levels)} 个 / en {len(en_levels)} 个",
                }
            )
    return findings


CHECKS = {
    "facts": check_facts,
    "structure": check_structure,
    "bilingual": check_bilingual,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Aleph 文档事实/结构/双语门")
    parser.add_argument("--check", default="all", choices=["all", *CHECKS.keys()])
    parser.add_argument("--docs", default="content/docs", help="文档内容根（相对文档仓）")
    parser.add_argument("--docs-repo", default=".", help="文档仓自身路径")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--baseline", default=str(Path(__file__).resolve().parent / "baseline.json"))
    parser.add_argument("--update-baseline", action="store_true", help="把当前失效集合写回基线（棘轮）")
    args = parser.parse_args()

    docs_repo = Path(args.docs_repo).resolve()
    content_root = (docs_repo / args.docs).resolve()
    if not content_root.is_dir():
        print(f"找不到文档内容目录：{content_root}", file=sys.stderr)
        return 2

    selected = list(CHECKS) if args.check == "all" else [args.check]
    baseline = load_baseline(Path(args.baseline))
    results = {}
    new_total = 0
    for name in selected:
        findings = CHECKS[name](content_root)
        keys = [f"{f['kind']}|{f['file']}|{f['reason']}" for f in findings]
        new_keys, known_keys = split_violations(keys, baseline.get(name, []))
        if args.update_baseline:
            fixed = update_section(name, keys, Path(args.baseline))
            print(f"基线已棘轮：{name} 段 {len(keys)} 条，修掉 {len(fixed)} 条")
            for item in fixed:
                print(f"  FIXED {item}")
            new_keys, known_keys = [], keys
        new_total += len(new_keys)
        results[name] = {
            "findings": findings,
            "new": new_keys,
            "known": known_keys,
        }

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for name in selected:
            entry = results[name]
            findings = entry["findings"]
            new_set = set(entry["new"])
            print(f"== {name}: {len(findings)} 项（新增 {len(entry['new'])}，基线旧债 {len(entry['known'])}）")
            for finding in findings:
                key = f"{finding['kind']}|{finding['file']}|{finding['reason']}"
                if key not in new_set:
                    continue
                line = finding.get("line", 0)
                location = f"{finding['file']}:{line}" if line else finding["file"]
                print(f"  {location}: {finding['reason']}")
                if finding.get("text"):
                    print(f"      | {finding['text']}")
    return 1 if new_total else 0


if __name__ == "__main__":
    sys.exit(main())
