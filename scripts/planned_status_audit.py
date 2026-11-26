#!/usr/bin/env python3
"""G1e: the planned-status gate.

A section that tells the reader "this is not on `main` yet" goes stale the
moment the work lands. This gate reads every 规划中 / Planned section and
checks that what the section claims is still true in the code repository:

* the section carries its status marker in the page's own language;
* every commit it names still exists;
* no commit it names has landed on `main`;
* no branch it names has been merged into `main`;
* no path it points at has landed on `main`.

A failure means the section has to be rewritten as current state — the
alternative is a page that tells the reader to look for something that is
already in the product.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gate_baseline import load_baseline, split_violations, update_section

HEADING_RE = re.compile(r"^(#{2,6})\s+(.*)$")
PLANNED_TITLE_RE = re.compile(r"(规划中|Planned)", re.IGNORECASE)
CODE_TOKEN_RE = re.compile(r"`([^`\n]+)`")
SHA_RE = re.compile(r"^[0-9a-f]{8,40}$")
PATH_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_./-]*\.[A-Za-z0-9]+$")
# A marker written in the other language: the section claims to be planned,
# but the reader gets a Chinese (or English) status line on a page that is
# written in the other language.
ZH_MARKER_RE = re.compile(r"状态：\s*规划中")
EN_MARKER_RE = re.compile(r"Status:\s*planned", re.IGNORECASE)
# Words that put a reference into a historical context: the commit is
# already on main and the section is talking about the past.
HISTORY_RE = re.compile(
    r"(之前|以前|早期|历史|当时|原先|已合并|合并后|撤回|退役|废弃|曾经"
    r"|\bhistory\b|\bhistor\w*\b|\bearlier\b|\bbefore\b|\bprevious\b|\bformer\b"
    r"|\boriginal\b|\bretired\b|\bremoved\b|\bdeprecated\b|\bmerged\b|\bwas\b)",
    re.IGNORECASE,
)


def git(repo: Path, *args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True
    )
    return proc.returncode, proc.stdout.strip()


def collect_sections(docs: Path) -> list[tuple[str, int, str, list[tuple[int, str]]]]:
    """Return (page, heading line, title, body lines) for every planned section."""
    sections: list[tuple[str, int, str, list[tuple[int, str]]]] = []
    for path in sorted(docs.rglob("*.mdx")):
        lines = path.read_text(encoding="utf-8").splitlines()
        relative = str(path.relative_to(docs))
        heading: tuple[int, str, int] | None = None
        body: list[tuple[int, str]] = []
        in_code = False
        for number, line in enumerate(lines, 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            match = HEADING_RE.match(line)
            if match:
                if heading is not None:
                    sections.append((relative, heading[2], heading[1], body))
                    heading, body = None, []
                level, title = len(match.group(1)), match.group(2)
                if PLANNED_TITLE_RE.search(title):
                    heading = (level, title, number)
                continue
            if heading is not None:
                body.append((number, line))
        if heading is not None:
            sections.append((relative, heading[2], heading[1], body))
    return sections


def audit(
    docs: Path,
    repo: Path,
) -> tuple[list[str], dict]:
    violations: list[str] = []
    stats = {"sections": 0, "zh": 0, "en": 0, "commits": 0, "branches": 0}
    main_exists = git(repo, "rev-parse", "--verify", "main")[0] == 0
    if not main_exists:
        violations.append("code repository has no `main` branch to compare against")

    for relative, heading_line, title, body in collect_sections(docs):
        stats["sections"] += 1
        language = "zh" if relative.startswith("zh/") else "en"
        stats[language] += 1
        text = "\n".join(line for _, line in body)

        tokens = CODE_TOKEN_RE.findall(text)
        commits = [token for token in tokens if SHA_RE.match(token)]
        # A branch reference is a name the code repository actually knows.
        # Anything else (a spec name, a command line) is not a branch.
        branches = [
            token
            for token in tokens
            if "-" in token
            and " " not in token
            and "/" not in token
            and not PATH_RE.match(token)
            and git(repo, "rev-parse", "--verify", f"refs/heads/{token}")[0] == 0
        ]
        paths = [token for token in tokens if PATH_RE.match(token)]
        stats["commits"] += len(commits)
        stats["branches"] += len(branches)

        # The section talks about what is (not) on main, so it has to say so
        # in the language of the page it lives on.
        if commits or branches:
            if language == "zh" and ZH_MARKER_RE.search(text) is None:
                violations.append(
                    f"{relative}:{heading_line}: 规划中小节引用了分支/提交但没有中文状态标记"
                )
            if language == "en" and EN_MARKER_RE.search(text) is None:
                violations.append(
                    f"{relative}:{heading_line}: planned section cites a branch or commit "
                    "but has no English status marker"
                )
        if language == "zh" and EN_MARKER_RE.search(text):
            violations.append(
                f"{relative}:{heading_line}: 中文小节里出现英文状态标记（Status: planned）"
            )
        if language == "en" and ZH_MARKER_RE.search(text):
            violations.append(
                f"{relative}:{heading_line}: 英文小节里出现中文状态标记（状态：规划中）"
            )

        for commit in commits:
            code, _ = git(repo, "cat-file", "-e", f"{commit}^{{commit}}")
            if code != 0:
                violations.append(
                    f"{relative}:{heading_line}: 引用的提交 {commit} 在代码仓里不存在"
                )
                continue
            code, _ = git(repo, "merge-base", "--is-ancestor", commit, "main")
            if code == 0:
                history = any(HISTORY_RE.search(line) for _, line in body)
                if not history:
                    violations.append(
                        f"{relative}:{heading_line}: 引用的提交 {commit} 已经合入 main，"
                        "本节仍写成规划中"
                    )

        for branch in branches:
            code, _ = git(repo, "merge-base", "--is-ancestor", branch, "main")
            if code == 0:
                violations.append(
                    f"{relative}:{heading_line}: 分支 {branch} 已经合并进 main，"
                    "本节仍写成规划中"
                )

        # A path the section points at must not have landed on main while the
        # section still describes it as unmerged work.
        for branch in branches:
            code, base = git(repo, "merge-base", "main", branch)
            if code != 0:
                continue
            code, changed = git(repo, "diff", "--name-only", f"{base}..{branch}")
            if code != 0:
                continue
            # The paths the branch introduced.  If one of them is on main
            # now, the work landed — even when the branch was squashed and
            # its tip is therefore not an ancestor of main.
            introduced = {path for path in changed.splitlines() if path}
            for path in paths:
                if path not in introduced:
                    continue
                if git(repo, "cat-file", "-e", f"main:{path}")[0] == 0:
                    violations.append(
                        f"{relative}:{heading_line}: 路径 {path} 已经在 main 上，"
                        "本节仍写成未合并分支里的东西"
                    )
    return violations, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="规划中状态门")
    parser.add_argument("--repo", default="../Aleph")
    parser.add_argument("--docs", default="content/docs")
    parser.add_argument("--baseline", default=str(Path(__file__).resolve().parent / "baseline.json"))
    parser.add_argument("--update-baseline", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    docs = Path(args.docs).resolve()
    repo = Path(args.repo).resolve()
    violations, stats = audit(docs, repo)

    baseline_path = Path(args.baseline)
    known = load_baseline(baseline_path).get("planned_stale", [])
    if args.update_baseline:
        dropped = update_section("planned_stale", violations, baseline_path)
        for item in dropped:
            print(f"已修复：{item}")

    new, old = split_violations(violations, known)
    if args.json:
        print(json.dumps({"new": new, "known": old}, ensure_ascii=False, indent=2))
    else:
        print(
            f"规划中小节 {stats['sections']}（zh {stats['zh']} / en {stats['en']}），"
            f"引用提交 {stats['commits']} 次、分支 {stats['branches']} 次，"
            f"失效 {len(violations)}（新增 {len(new)}，基线旧债 {len(old)}）"
        )
        for item in new:
            print(f"NEW  {item}")
        for item in old:
            print(f"OLD  {item}")
    return 1 if new else 0


if __name__ == "__main__":
    raise SystemExit(main())
