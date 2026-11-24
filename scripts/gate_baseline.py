#!/usr/bin/env python3
"""Baseline ratchet shared by the documentation gates.

A gate reports two kinds of findings:

* known  — already recorded in the baseline file (the debt we have accepted
  for this phase). They are printed for information but do not fail the gate.
* new    — findings the baseline does not know about. These fail the gate.

After a phase repairs some of the debt, run the gate with
`--update-baseline` to ratchet the baseline down to what is still broken. The
baseline never grows silently: growing only happens through an explicit
`--update-baseline` call, and the printed diff shows what was added.
"""

from __future__ import annotations

import json
from pathlib import Path

BASELINE_PATH = Path(__file__).resolve().parent / "baseline.json"


def load_baseline(path: Path = BASELINE_PATH) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_baseline(data: dict, path: Path = BASELINE_PATH) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def split_violations(keys: list[str], baseline_keys: list[str]) -> tuple[list[str], list[str]]:
    """Return (new, known) given the current violation keys and the baseline."""
    baseline = set(baseline_keys)
    new = [key for key in keys if key not in baseline]
    known = [key for key in keys if key in baseline]
    return new, known


def update_section(section: str, keys: list[str], path: Path = BASELINE_PATH) -> list[str]:
    """Ratchet one section down to the current violation set.

    Returns the keys that were dropped from the baseline (now fixed).
    """
    data = load_baseline(path)
    previous = set(data.get(section, []))
    current = set(keys)
    data[section] = sorted(current)
    save_baseline(data, path)
    return sorted(previous - current)
