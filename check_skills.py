#!/usr/bin/env python3
"""Structural checks for the skills in this repo.

Checks, per skill:
  - SKILL.md has YAML frontmatter with `name` and `description`
  - frontmatter is under the 1024-character limit
  - `name` uses only [A-Za-z0-9-]
  - no two skills declare the same `name`
  - every /terebentina:<name> reference resolves to a declared skill
  - every relative markdown link resolves to a file that exists
  - no agents/openai.yaml sits beside a missing SKILL.md

Exit code 0 means every check passed. Run it from anywhere:
    python3 check_skills.py
"""
import re
import sys
import pathlib

root = pathlib.Path(__file__).resolve().parent
skills_dir = root / "skills"
fails, warns = [], []


def prose_lines(path):
    """Yield (lineno, line), skipping fenced code blocks."""
    fenced = False
    for i, line in enumerate(path.read_text().splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            yield i, line


# --- collect declared skill names --------------------------------------------
declared = {}
for p in sorted(skills_dir.glob("*/SKILL.md")):
    text = p.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fails.append(f"{p.relative_to(root)}: no YAML frontmatter")
        continue
    fm = m.group(1)
    if len(fm) > 1024:
        fails.append(f"{p.relative_to(root)}: frontmatter {len(fm)} chars > 1024 limit")
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    if not re.search(r"^description:", fm, re.M):
        fails.append(f"{p.relative_to(root)}: frontmatter has no `description`")
    if not name:
        fails.append(f"{p.relative_to(root)}: frontmatter has no `name`")
        continue
    n = name.group(1).strip()
    if not re.fullmatch(r"[A-Za-z0-9-]+", n):
        fails.append(f"{p.relative_to(root)}: name {n!r} has chars outside [A-Za-z0-9-]")
    if n in declared:
        fails.append(f"duplicate skill name {n!r}: {p.relative_to(root)} and {declared[n]}")
    declared[n] = p.relative_to(root)
    if n != p.parent.name:
        warns.append(f"{p.relative_to(root)}: name {n!r} != directory {p.parent.name!r}")

# --- every /terebentina:X resolves to a declared skill ------------------------
for p in sorted(skills_dir.rglob("*.md")):
    for i, line in enumerate(p.read_text().splitlines(), 1):
        for ref in re.findall(r"/terebentina:([a-z0-9-]+)", line):
            if ref not in declared:
                fails.append(f"{p.relative_to(root)}:{i}: dangling ref /terebentina:{ref}")

# --- every relative markdown link resolves -----------------------------------
for p in sorted(skills_dir.rglob("*.md")):
    for i, line in prose_lines(p):
        for target in re.findall(r"\]\((\./[^)#]+|[A-Z][A-Za-z0-9-]*\.md)[^)]*\)", line):
            if not (p.parent / target).exists():
                fails.append(f"{p.relative_to(root)}:{i}: broken link -> {target}")

# --- no orphaned agent manifests ---------------------------------------------
for p in sorted(skills_dir.glob("*/agents/openai.yaml")):
    if not (p.parent.parent / "SKILL.md").exists():
        fails.append(f"{p.relative_to(root)}: agent yaml with no SKILL.md")

print(f"skills declared: {len(declared)}")
for n in sorted(declared):
    print(f"  {n}")
print()
for w in warns:
    print(f"WARN  {w}")
for f in fails:
    print(f"FAIL  {f}")
print(f"\n{len(fails)} failures, {len(warns)} warnings")
sys.exit(1 if fails else 0)
