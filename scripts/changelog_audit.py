#!/usr/bin/env python3
"""G1f: the changelog reconciliation gate.

The site carries a documentation-focused changelog; the code repository
carries the release record. The two drift apart in both directions: the
site can describe a release that upstream never shipped, and upstream can
ship a release the site never mentions. This gate checks that they agree.

Checks:
  * every version the site documents exists upstream;
  * every upstream version from the site's oldest documented version on
    (the coverage boundary) is documented on the site;
  * the upstream `VERSION` file names a release the site documents;
  * the zh and en pages carry the same version and date entries;
  * no page lists a version twice;
  * the coverage date in the frontmatter matches the newest date entry;
  * the site's newest rolling entry is not older than upstream's.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gate_baseline import load_baseline, split_violations, update_section

UPSTREAM_VERSION_RE = re.compile(r"^##\s*\[(\d+(?:\.\d+)*)\]")
UPSTREAM_DATE_RE = re.compile(r"^##\s*(\d{4}-\d{2}-\d{2})\b")
SITE_VERSION_RE = re.compile(r"^##\s*(\d+\.\d+(?:\.\d+)*)\b")
SITE_DATE_RE = re.compile(r"^##\s*(\d{4}-\d{2}-\d{2})\b")
FRONTMATTER_DATE_RE = re.compile(r"(?:截至|through)\s*(\d{4}-\d{2}-\d{2})")


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def parse_upstream(changelog: Path) -> tuple[list[str], list[str]]:
    versions: list[str] = []
    dates: list[str] = []
    for line in changelog.read_text(encoding="utf-8").splitlines():
        match = UPSTREAM_VERSION_RE.match(line)
        if match:
            versions.append(match.group(1))
            continue
        match = UPSTREAM_DATE_RE.match(line)
        if match:
            dates.append(match.group(1))
    return versions, dates


def parse_site(page: Path) -> tuple[list[str], list[str], str | None]:
    text = page.read_text(encoding="utf-8")
    versions: list[str] = []
    dates: list[str] = []
    for line in text.splitlines():
        match = SITE_DATE_RE.match(line)
        if match:
            dates.append(match.group(1))
            continue
        match = SITE_VERSION_RE.match(line)
        if match:
            versions.append(match.group(1))
    frontmatter = ""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
    claim = FRONTMATTER_DATE_RE.search(frontmatter)
    return versions, dates, claim.group(1) if claim else None


def audit(docs: Path, repo: Path) -> tuple[list[str], dict]:
    violations: list[str] = []
    stats: dict[str, int] = {}

    changelog = repo / "CHANGELOG.md"
    version_file = repo / "VERSION"
    if not changelog.exists():
        return ["code repository has no CHANGELOG.md to reconcile against"], stats
    upstream_versions, upstream_dates = parse_upstream(changelog)
    upstream_set = set(upstream_versions)
    stats["upstream_versions"] = len(upstream_set)
    stats["upstream_dates"] = len(upstream_dates)

    pages: dict[str, tuple[list[str], list[str], str | None]] = {}
    for language in ("zh", "en"):
        page = docs / language / "changelog.mdx"
        if not page.exists():
            violations.append(f"{language}/changelog.mdx: 缺少更新日志页面")
            continue
        pages[language] = parse_site(page)

    for language, (versions, dates, claim) in pages.items():
        stats[f"{language}_versions"] = len(versions)
        stats[f"{language}_dates"] = len(dates)
        for version in versions:
            if version not in upstream_set:
                violations.append(
                    f"{language}/changelog.mdx: 版本 {version} 在上游 CHANGELOG.md 里不存在"
                )
        duplicates = {v for v in versions if versions.count(v) > 1}
        for version in sorted(duplicates):
            violations.append(
                f"{language}/changelog.mdx: 版本 {version} 出现了不止一次"
            )
        if dates and claim and claim != dates[0]:
            violations.append(
                f"{language}/changelog.mdx: frontmatter 说覆盖到 {claim}，"
                f"但最新的日期条目是 {dates[0]}"
            )
        if dates and not claim:
            violations.append(
                f"{language}/changelog.mdx: frontmatter 没有写覆盖到哪一天"
            )

    if "zh" in pages and "en" in pages:
        zh_versions, zh_dates, _ = pages["zh"]
        en_versions, en_dates, _ = pages["en"]
        if set(zh_versions) != set(en_versions):
            only_zh = sorted(set(zh_versions) - set(en_versions))
            only_en = sorted(set(en_versions) - set(zh_versions))
            violations.append(
                f"changelog.mdx: 中英文版本集合不一致（仅 zh: {only_zh}；仅 en: {only_en}）"
            )
        if set(zh_dates) != set(en_dates):
            only_zh = sorted(set(zh_dates) - set(en_dates))
            only_en = sorted(set(en_dates) - set(zh_dates))
            violations.append(
                f"changelog.mdx: 中英文日期条目不一致（仅 zh: {only_zh}；仅 en: {only_en}）"
            )

    # The site documents the releases from its oldest documented version on.
    # Every upstream release inside that window has to be on the site.
    site_versions = set(pages.get("zh", ([], [], None))[0])
    if site_versions:
        boundary = min(site_versions, key=version_key)
        missing = sorted(
            (version for version in upstream_set if version_key(version) >= version_key(boundary)),
            key=version_key,
        )
        for version in missing:
            if version not in site_versions:
                violations.append(
                    f"changelog.mdx: 上游版本 {version} 不在站点更新日志里"
                    f"（站点覆盖边界 {boundary}）"
                )
        stats["coverage_boundary"] = boundary

    if version_file.exists():
        current = version_file.read_text(encoding="utf-8").strip()
        if current and current not in site_versions:
            violations.append(
                f"changelog.mdx: 上游 VERSION 是 {current}，站点更新日志里没有这个版本"
            )
        stats["version_file"] = current

    site_dates = set(pages.get("zh", ([], [], None))[1])
    if upstream_dates and site_dates:
        if max(upstream_dates) > max(site_dates):
            violations.append(
                f"changelog.mdx: 上游最新滚动条目是 {max(upstream_dates)}，"
                f"站点最新是 {max(site_dates)}，站点落后"
            )
    return violations, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="更新日志对账门")
    parser.add_argument("--repo", default="../Aleph")
    parser.add_argument("--docs", default="content/docs")
    parser.add_argument(
        "--baseline", default=str(Path(__file__).resolve().parent / "baseline.json")
    )
    parser.add_argument("--update-baseline", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    docs = Path(args.docs).resolve()
    repo = Path(args.repo).resolve()
    violations, stats = audit(docs, repo)

    baseline_path = Path(args.baseline)
    known = load_baseline(baseline_path).get("changelog_drift", [])
    if args.update_baseline:
        dropped = update_section("changelog_drift", violations, baseline_path)
        for item in dropped:
            print(f"已修复：{item}")

    new, old = split_violations(violations, known)
    if args.json:
        print(json.dumps({"new": new, "known": old}, ensure_ascii=False, indent=2))
    else:
        print(
            f"上游版本 {stats.get('upstream_versions', 0)} 个，"
            f"站点 zh {stats.get('zh_versions', 0)} / en {stats.get('en_versions', 0)} 个，"
            f"覆盖边界 {stats.get('coverage_boundary', '-')}，"
            f"失效 {len(violations)}（新增 {len(new)}，基线旧债 {len(old)}）"
        )
        for item in new:
            print(f"NEW  {item}")
        for item in old:
            print(f"OLD  {item}")
    return 1 if new else 0


if __name__ == "__main__":
    raise SystemExit(main())
