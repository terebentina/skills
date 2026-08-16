---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

Spin up a **background agent** to do the research, so you keep working while it reads.

**Write all prose in ASD-STE100 Simplified Technical English** — the findings file and your messages to the user. **REQUIRED SUB-SKILL:** `domain-modeling`. Name that skill in the background agent's brief, and tell it that quotations from a source keep their original wording.

## Wayfinder use

When `wayfinder` calls this skill, save the report under `.scratch/wayfinder/<effort>/`.

This section replaces the report location rule below for Wayfinder work.

Treat all other paths as read-only. Do not create branches, worktrees, commits, issue changes, ADRs, or glossary updates.

Pass the effort path and this boundary to the background agent. Link the report from its Wayfinder ticket.

Its job:

1. Investigate the question against **primary sources** — official docs, source code, specs, first-party APIs — not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
