#!/usr/bin/env python3
"""Suggest real names for stale dotted tokens found in the docs.

Given dotted tokens (method names, config keys, struct fields), look for
plausible current counterparts in:

* the gateway method census (``src/gateway/method_census.rs``),
* every dotted string literal in the Aleph source tree.

The suggestions are ranked by similarity so a human or a writing agent can
confirm the replacement instead of guessing.

Usage:
    python3 scripts/suggest_names.py --repo ../Aleph --tokens a.b c.d
    python3 scripts/suggest_names.py --repo ../Aleph --file /tmp/r5/ghosts_by_file.txt
    cat tokens.txt | python3 scripts/suggest_names.py --repo ../Aleph --stdin
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

CENSUS_RE = re.compile(r'\(\s*"([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)"\s*,\s*Class::(Admin|Open)')
LITERAL_RE = re.compile(r'"([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)"')
SOURCE_DIRS = ("src", "shared", "interfaces", "desktop", "crates")
SOURCE_SUFFIXES = (".rs",)


def census_methods(repo: Path) -> dict[str, str]:
    path = repo / "src" / "gateway" / "method_census.rs"
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for name, cls in CENSUS_RE.findall(path.read_text(encoding="utf-8", errors="replace")):
        out[name] = cls
    return out


def code_literals(repo: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for root in SOURCE_DIRS:
        base = repo / root
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.suffix not in SOURCE_SUFFIXES or not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for match in LITERAL_RE.findall(text):
                rel = path.relative_to(repo).as_posix()
                if rel not in out[match]:
                    out[match].append(rel)
    return out


def candidates(token: str, census: dict[str, str], literals: dict[str, list[str]]) -> list[tuple[str, str, str]]:
    """Return (name, kind, where) tuples ranked by similarity to ``token``."""
    prefix = token.split(".")[0] + "."
    namespace = token.split(".")[0]
    pool: dict[str, tuple[str, str]] = {}
    for name, cls in census.items():
        pool[name] = ("method", cls)
    for name, files in literals.items():
        if name not in pool:
            pool[name] = ("literal", files[0])

    scored: list[tuple[float, str, str, str]] = []
    for name, (kind, where) in pool.items():
        if name == token:
            continue
        score = 0.0
        if name.startswith(prefix):
            score += 0.55
        if name.split(".")[0] == namespace:
            score += 0.2
        ratio = difflib.SequenceMatcher(None, token, name).ratio()
        score += 0.45 * ratio
        if name.startswith(namespace + "."):
            score += 0.05
        if kind == "method":
            score += 0.05
        if score < 0.34:
            continue
        scored.append((score, name, kind, where))
    scored.sort(reverse=True)
    return [(name, kind, where) for score, name, kind, where in scored[:8]]


def read_tokens(args: argparse.Namespace) -> list[str]:
    tokens: list[str] = []
    if args.tokens:
        tokens.extend(args.tokens)
    if args.file:
        for line in Path(args.file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Accept "token" or "L12: token" or "  - token" forms.
            for piece in line.replace("`", " ").split():
                if ":" in piece and piece.split(":", 1)[0].isdigit():
                    piece = piece.split(":", 1)[1]
                if piece and "." in piece and not piece.startswith(("http", "/")):
                    tokens.append(piece)
    if args.stdin:
        tokens.extend(sys.stdin.read().split())
    seen: set[str] = set()
    ordered: list[str] = []
    for token in tokens:
        if token not in seen:
            seen.add(token)
            ordered.append(token)
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="../Aleph", help="path to the Aleph source repository")
    parser.add_argument("--tokens", nargs="*", default=[])
    parser.add_argument("--file")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    census = census_methods(repo)
    literals = code_literals(repo)
    tokens = read_tokens(args)

    report: dict[str, list[dict[str, str]]] = {}
    for token in tokens:
        found = candidates(token, census, literals)
        report[token] = [
            {"name": name, "kind": kind, "where": where} for name, kind, where in found
        ]

    if args.json:
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    for token in tokens:
        print(f"\n{token}")
        if token in census:
            print(f"  [census] Class::{census[token]}")
        if token in literals:
            print(f"  [literal] {', '.join(literals[token][:3])}")
        found = report[token]
        if not found:
            print("  (无近似候选 —— 该名称在代码中已不存在，需按语义重写或删除)")
            continue
        for item in found:
            print(f"  -> {item['name']:<44} {item['kind']:<8} {item['where']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
