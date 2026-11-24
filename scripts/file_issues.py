#!/usr/bin/env python3
"""Per-file issue list: broken anchors and ghost method tokens, with candidates.

Usage:
    python3 scripts/file_issues.py --repo ../Aleph --files FILE [FILE ...]
    python3 scripts/file_issues.py --repo ../Aleph --files-from /tmp/r5/concepts.txt
    python3 scripts/file_issues.py --repo ../Aleph --files-from X --json

Prints, for every given content file (zh and en are separate entries):
  * ANCHOR  file:line  token        -> nearest existing path, if any
  * METHOD  file:line  token        -> candidate real names (census / code literal)

The candidate list is a hint, not an answer: every fix must be confirmed by
reading the code. A token whose subject no longer exists must be rewritten or
removed, not renamed to something plausible.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SOURCE_PREFIXES = (
    "src/",
    "desktop/",
    "shared/",
    "crates/",
    "interfaces/",
    "plugins/",
    "scripts/",
    "qa/",
    "tests/",
    "docs/",
)
ROOT_FILES = (
    "Cargo.toml",
    "Cargo.lock",
    "justfile",
    "config.search.example.toml",
    "CHANGELOG.md",
    "AGENTS.md",
    "CLAUDE.md",
    "package.json",
    "pnpm-lock.yaml",
)

PATH_IN_TEXT = re.compile(r"`([^`\n]{2,200})`")
TOKEN_IN_TEXT = re.compile(r"`([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)`")
CENSUS_ENTRY = re.compile(r'\(\s*"([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)"\s*,\s*Class::(Admin|Open)')
CODE_LITERAL = re.compile(r'"([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)"')

PATH_NOISE = re.compile(r"[{}*<>$|\\]")


SKIP_DIRS = {"node_modules", "target", "dist", ".git", ".next", "build"}

# 锚点判定用的目录遍历：Aleph 仓把构建好的 Panel 产物（interfaces/webchat/dist/）
# 一起提交进 git，所以锚点扫描**不能**跳过 dist，否则会误报。
SKIP_DIRS_FOR_ANCHORS = {"node_modules", "target", ".git", ".next", "build"}


def repo_files(repo: Path) -> set[str]:
    out: set[str] = set()
    for base in ("src", "desktop", "shared", "crates", "interfaces", "plugins", "scripts", "qa", "tests", "docs"):
        root = repo / base
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS_FOR_ANCHORS]
            for name in filenames:
                out.add(os.path.relpath(os.path.join(dirpath, name), repo))
    for name in ROOT_FILES:
        if (repo / name).exists():
            out.add(name)
    return out


def repo_dirs(repo: Path) -> set[str]:
    """Every directory under the tracked roots, as repo-relative paths with a trailing slash."""
    out: set[str] = set()
    for base in ("src", "desktop", "shared", "crates", "interfaces", "plugins", "scripts", "qa", "tests", "docs"):
        root = repo / base
        if not root.exists():
            continue
        for dirpath, dirnames, _ in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS_FOR_ANCHORS]
            for name in dirnames:
                out.add(os.path.relpath(os.path.join(dirpath, name), repo) + "/")
    return out


def code_tokens(repo: Path) -> dict[str, list[str]]:
    """Every dotted lowercase literal in the code, mapped to where it appears."""
    found: dict[str, list[str]] = {}
    for base in ("src", "shared", "interfaces", "desktop", "crates"):
        root = repo / base
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                if not name.endswith(".rs"):
                    continue
                path = Path(dirpath) / name
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                rel = str(path.relative_to(repo))
                for match in CODE_LITERAL.finditer(text):
                    found.setdefault(match.group(1), []).append(rel)
    return found


def census_methods(repo: Path) -> dict[str, str]:
    path = repo / "src/gateway/method_census.rs"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    return {m.group(1): m.group(2) for m in CENSUS_ENTRY.finditer(text)}


def clean_path_token(raw: str) -> str | None:
    token = raw.strip()
    if token.startswith("/") or "://" in token:
        return None
    token = token.split("::")[0].split("#")[0].split(":")[0].strip()
    if not token or PATH_NOISE.search(token):
        return None
    if token.startswith(SOURCE_PREFIXES):
        return token
    if token in ROOT_FILES:
        return token
    return None


def suggest_path(token: str, existing: set[str]) -> list[str]:
    tail = token.rsplit("/", 1)[-1]
    if not tail:
        return []
    stem = tail.rsplit(".", 1)[0]
    exact = sorted(p for p in existing if p.rsplit("/", 1)[-1] == tail)
    if exact:
        return exact[:4]
    same_stem = sorted(p for p in existing if p.rsplit("/", 1)[-1].rsplit(".", 1)[0] == stem)
    if same_stem:
        return same_stem[:4]
    names = {p.rsplit("/", 1)[-1] for p in existing}
    close = difflib.get_close_matches(tail, names, n=4, cutoff=0.6)
    stems = difflib.get_close_matches(stem, {n.rsplit(".", 1)[0] for n in names}, n=4, cutoff=0.6)
    out = []
    for match in close + stems:
        for path in sorted(existing):
            if path.rsplit("/", 1)[-1] == match:
                out.append(path)
                break
    return out[:4]


def suggest_method(token: str, literals: dict[str, list[str]], methods: dict[str, str]) -> list[str]:
    namespace = token.split(".", 1)[0]
    names = [t for t in literals if t.startswith(namespace + ".")]
    close = difflib.get_close_matches(token, names, n=5, cutoff=0.55)
    if not close:
        close = sorted(names)[:5]
    out = []
    for candidate in close:
        if candidate in methods:
            out.append(f"{candidate} (census Class::{methods[candidate]})")
        else:
            where = literals[candidate][0] if literals[candidate] else "?"
            out.append(f"{candidate} (code literal, {where})")
    return out


def collect(files: list[str], repo: Path) -> list[dict]:
    existing = repo_files(repo)
    existing_dirs = repo_dirs(repo)
    literals = code_tokens(repo)
    methods = census_methods(repo)
    issues: list[dict] = []
    for rel in files:
        path = REPO_ROOT / rel
        if not path.exists():
            issues.append({"kind": "missing-file", "file": rel, "line": 0, "token": "", "candidates": []})
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if lineno <= 2:
                continue
            for raw in PATH_IN_TEXT.findall(line):
                token = clean_path_token(raw)
                if token and token not in existing and token not in existing_dirs:
                    issues.append({
                        "kind": "anchor", "file": rel, "line": lineno, "token": token,
                        "candidates": suggest_path(token, existing),
                    })
            for token in TOKEN_IN_TEXT.findall(line):
                if token.split(".", 1)[0] in {"src", "desktop", "shared", "crates", "interfaces", "docs", "scripts", "qa", "tests", "content", "config"}:
                    continue
                if token in literals or token in methods:
                    continue
                issues.append({
                    "kind": "method", "file": rel, "line": lineno, "token": token,
                    "candidates": suggest_method(token, literals, methods),
                })
    return issues


def read_file_list(args: argparse.Namespace) -> list[str]:
    files: list[str] = []
    if args.files:
        files.extend(args.files)
    if args.files_from:
        text = Path(args.files_from).read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("## "):
                line = line[3:].strip()
                line = re.sub(r"\s*\(\d+.*\)\s*$", "", line)
            if line.startswith("content/"):
                files.append(line)
    seen: set[str] = set()
    unique = []
    for item in files:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default="../Aleph")
    parser.add_argument("--files", nargs="*", default=[])
    parser.add_argument("--files-from", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    issues = collect(read_file_list(args), repo)
    if args.json:
        print(json.dumps(issues, ensure_ascii=False, indent=2))
        return 0

    by_file: dict[str, list[dict]] = {}
    for issue in issues:
        by_file.setdefault(issue["file"], []).append(issue)
    for rel in sorted(by_file):
        print(f"## {rel}")
        for issue in by_file[rel]:
            head = f"  L{issue['line']}  {issue['kind']}: {issue['token']}"
            print(head)
            for candidate in issue["candidates"]:
                print(f"      -> {candidate}")
        print()
    total = len(issues)
    print(f"total issues: {total} across {len(by_file)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
