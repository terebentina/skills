#!/usr/bin/env python3
"""Cross-host structural checks for the skills in this repository.

Checks, per skill:
  - SKILL.md has YAML frontmatter with `name` and `description`
  - shared frontmatter contains no host-specific fields
  - frontmatter is under the 1024-character limit
  - `name` uses lowercase hyphen-case and matches its directory
  - no two skills declare the same `name`
  - agents/openai.yaml contains complete Codex interface metadata
  - every relative markdown link resolves to a file that exists
  - no agents/openai.yaml sits beside a missing SKILL.md
  - Claude and Codex plugin metadata agree on the plugin identity and version

Exit code 0 means every check passed. Run it from anywhere:
    python3 check_skills.py
"""
import json
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent
skills_dir = root / "skills"
fails, warns = [], []
explicit_only = {
    "handoff",
    "implement",
    "improve-codebase-architecture",
    "setup",
    "to-spec",
    "to-tickets",
    "triage",
    "wayfinder",
}


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
    fields = set(re.findall(r"^([a-z][a-z0-9-]*):", fm, re.M))
    unexpected = fields - {"name", "description"}
    if unexpected:
        fails.append(
            f"{p.relative_to(root)}: host-specific or unsupported frontmatter: "
            f"{', '.join(sorted(unexpected))}"
        )
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    if not re.search(r"^description:\s*\S", fm, re.M):
        fails.append(f"{p.relative_to(root)}: frontmatter has no `description`")
    if not name:
        fails.append(f"{p.relative_to(root)}: frontmatter has no `name`")
        continue
    n = name.group(1).strip()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", n):
        fails.append(f"{p.relative_to(root)}: name {n!r} is not lowercase hyphen-case")
    if len(n) > 64:
        fails.append(f"{p.relative_to(root)}: name {n!r} exceeds 64 characters")
    if n in declared:
        fails.append(f"duplicate skill name {n!r}: {p.relative_to(root)} and {declared[n]}")
    declared[n] = p.relative_to(root)
    if n != p.parent.name:
        fails.append(f"{p.relative_to(root)}: name {n!r} != directory {p.parent.name!r}")

# --- shared instructions stay host-neutral -----------------------------------
for p in sorted(skills_dir.rglob("*.md")):
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if re.search(r"/terebentina:[a-z0-9-]+", line):
            fails.append(f"{p.relative_to(root)}:{i}: Claude-only skill invocation syntax")
        for ref in re.findall(r"\$([a-z][a-z0-9-]+)", line):
            if ref in declared:
                fails.append(f"{p.relative_to(root)}:{i}: Codex-only skill invocation syntax")

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

# --- every skill has complete Codex UI metadata ------------------------------
for name, skill_path in sorted(declared.items()):
    skill_dir = root / skill_path.parent
    agent_path = skill_dir / "agents" / "openai.yaml"
    if not agent_path.is_file():
        fails.append(f"{agent_path.relative_to(root)}: missing Codex UI metadata")
        continue
    text = agent_path.read_text()
    display = re.search(r'^\s{2}display_name:\s*"([^"]+)"\s*$', text, re.M)
    short = re.search(r'^\s{2}short_description:\s*"([^"]+)"\s*$', text, re.M)
    prompt = re.search(r'^\s{2}default_prompt:\s*"([^"]+)"\s*$', text, re.M)
    if not display:
        fails.append(f"{agent_path.relative_to(root)}: missing quoted `interface.display_name`")
    if not short:
        fails.append(f"{agent_path.relative_to(root)}: missing quoted `interface.short_description`")
    elif not 25 <= len(short.group(1)) <= 64:
        fails.append(f"{agent_path.relative_to(root)}: short description must be 25-64 characters")
    if not prompt:
        fails.append(f"{agent_path.relative_to(root)}: missing quoted `interface.default_prompt`")
    elif f"${name}" not in prompt.group(1):
        fails.append(f"{agent_path.relative_to(root)}: default prompt must mention `${name}`")
    policy = re.search(r"^\s{2}allow_implicit_invocation:\s*(true|false)\s*$", text, re.M)
    if name in explicit_only and (not policy or policy.group(1) != "false"):
        fails.append(f"{agent_path.relative_to(root)}: explicit-only skill must disable implicit invocation")

# --- plugin manifests identify the same package ------------------------------
codex_manifest_path = root / ".codex-plugin" / "plugin.json"
claude_marketplace_path = root / ".claude-plugin" / "marketplace.json"
try:
    codex_manifest = json.loads(codex_manifest_path.read_text())
except (OSError, json.JSONDecodeError):
    fails.append(".codex-plugin/plugin.json: missing or invalid JSON")
    codex_manifest = {}
try:
    claude_marketplace = json.loads(claude_marketplace_path.read_text())
except (OSError, json.JSONDecodeError):
    fails.append(".claude-plugin/marketplace.json: missing or invalid JSON")
    claude_marketplace = {}

plugin_name = codex_manifest.get("name")
plugin_version = codex_manifest.get("version")
if not isinstance(plugin_name, str) or not plugin_name:
    fails.append(".codex-plugin/plugin.json: missing plugin name")
if not isinstance(plugin_version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", plugin_version):
    fails.append(".codex-plugin/plugin.json: version is not strict semantic versioning")
if codex_manifest.get("skills") != "./skills/":
    fails.append(".codex-plugin/plugin.json: `skills` must be `./skills/`")
claude_plugins = claude_marketplace.get("plugins", [])
claude_plugin = next(
    (item for item in claude_plugins if isinstance(item, dict) and item.get("name") == plugin_name),
    None,
)
if claude_plugin is None:
    fails.append(".claude-plugin/marketplace.json: matching plugin entry is missing")
elif claude_marketplace.get("metadata", {}).get("version") != plugin_version:
    fails.append("plugin version differs between Claude and Codex metadata")

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
