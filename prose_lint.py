#!/usr/bin/env python3
"""Find objective prose defects in this repository's Markdown files.

The checks stay narrow. Vocabulary and sentence quality need human judgment.

Usage:
    python3 prose_lint.py
    python3 prose_lint.py skills/triage/SKILL.md
"""

from pathlib import Path
import sys


FORBIDDEN_CHARACTERS = {
    "\u2014": "EM-DASH",
    "\u2018": "CURLY-QUOTE",
    "\u2019": "CURLY-QUOTE",
    "\u201c": "CURLY-QUOTE",
    "\u201d": "CURLY-QUOTE",
}

root = Path(__file__).resolve().parent
glossary_path = root / "skills/codebase-design/SKILL.md"
targets = [Path(arg) for arg in sys.argv[1:]]
if not targets:
    targets = [root / "README.md", *sorted((root / "skills").rglob("*.md"))]

failures = 0
for path in targets:
    fenced = False
    for line_number, line in enumerate(path.read_text().splitlines(keepends=True), 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if path.resolve() == glossary_path and line.startswith("**") and " \u2014 " in line:
            continue
        for character, code in FORBIDDEN_CHARACTERS.items():
            if character in line:
                print(f"{path}:{line_number}: {code}: {line.strip()}")
                failures += 1
        if line.rstrip("\n\r").endswith((" ", "\t")):
            print(f"{path}:{line_number}: TRAILING-SPACE: {line.rstrip()}")
            failures += 1

if failures:
    print(f"\n{failures} prose defect(s).")
    raise SystemExit(1)

print(f"Checked {len(targets)} Markdown file(s).")
