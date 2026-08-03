#!/usr/bin/env python3
"""Heuristic ASD-STE100 lint for the prose in this repo's skills.

Flags three of the rules in the `domain-modeling` skill's "Write in STE" section:
  LONG      rule 8  — a sentence over 25 words
  PASSIVE   rule 10 — a candidate passive construction
  ING-VERB  rule 5  — an -ing form used as a verb

It skips fenced code blocks, table rows, and headings, because the rewrite
tables hold non-STE text on purpose.

THIS TOOL ONLY FINDS CANDIDATES. Read every hit yourself. It cannot tell a
breach from a rule that quotes its own bad example, so it reports lines like
`Write "the test catches the bug", not "the bug is caught by the test"` as
passive. Never fix a hit without reading it.

Usage:
    python3 ste_lint.py                        # every skill
    python3 ste_lint.py skills/triage/SKILL.md # named files
"""
import re
import sys
import pathlib

PASSIVE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+"
    r"(\w+ed|done|written|made|given|taken|caught|read|kept|held)\b",
    re.I,
)
ING_VERB = re.compile(r"\b(is|are|was|were)\s+\w+ing\b", re.I)
MAX_WORDS = 25

root = pathlib.Path(__file__).resolve().parent
targets = [pathlib.Path(a) for a in sys.argv[1:]] or sorted((root / "skills").rglob("*.md"))

total = 0
for p in targets:
    hits = []
    fenced = False
    for i, line in enumerate(p.read_text().splitlines(), 1):
        s = line.strip()
        if s.startswith("```"):
            fenced = not fenced
            continue
        if fenced or s.startswith("|") or s.startswith("#") or not s:
            continue
        clean = re.sub(r"`[^`]*`", "X", s)
        clean = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", clean)
        clean = re.sub(r"[*_]", "", clean)
        clean = re.sub(r"^[-\d.]+\s*\[?[ x]?\]?\s*", "", clean)
        for sent in re.split(r"(?<=[.!?])\s+", clean):
            sent = sent.strip()
            if not sent:
                continue
            n = len(sent.split())
            if n > MAX_WORDS:
                hits.append(f"  L{i} LONG({n}w): {sent[:110]}")
            if PASSIVE.search(sent):
                hits.append(f"  L{i} PASSIVE?: {sent[:110]}")
            if ING_VERB.search(sent):
                hits.append(f"  L{i} ING-VERB?: {sent[:110]}")
    if hits:
        try:
            label = p.resolve().relative_to(root)
        except ValueError:
            label = p
        print(f"\n===== {label}")
        print("\n".join(hits))
        total += len(hits)

print(f"\n{total} candidates across {len(targets)} file(s). Read each one before you change it.")
