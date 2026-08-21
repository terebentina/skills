# Terebentina agent skills

This repository contains reusable skills for planning, research, design, diagnosis, and delivery.
Most skills started from Matt Pocock's work and include changes for this workflow.

The shared `SKILL.md` files use host-neutral instructions. Product-specific metadata stays in separate integration files.

## Install in Codex

Add this repository as a plugin marketplace:

```bash
codex plugin marketplace add terebentina/skills
```

Start Codex and run `/plugins`. Install the `terebentina` plugin, then start a new session.

## Install in Claude Code

```bash
claude plugins marketplace add terebentina/skills
```

## Install in another Agent Skills host

```bash
npx skills@latest add terebentina/skills
```

## Thanks

Thanks to [Matt Pocock](https://github.com/mattpocock) for his teaching and original skills.
