---
name: setup
description: Configure the issue tracker, triage labels, and domain docs for these engineering skills. Use only when the user asks for setup.
disable-model-invocation: true
---

# Setup engineering skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker.** Where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels.** The strings used for the five canonical triage roles
- **Domain docs.** Where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`. Is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root. Does either file exist? Does either file contain an `## Agent skills` section?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`. Does this skill's prior output already exist?
- `.scratch/`. Sign that a local-markdown issue tracker convention is already in use
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals such as `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or packages under `packages/*` with their own `src/` directories. Offer multi-context setup only when these signals exist.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo).

**Section A. Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, `to-spec` read from and write to it. They need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub.** Issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab.** Issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Jira.** Issues live in your Jira instance (uses the [`jira`](https://github.com/ankitpokhrel/jira-cli) CLI). No automatic detection from `git remote`. User picks this manually.
- **Local markdown.** Issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other**, such as Linear or Shortcut. Ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates disable triage for external pull or merge requests by default. Leave that setting off unless the user changes it later.

**Section B. Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you). An uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`.

On **yes**, write them as-is. On **no**, collect the existing label for each role so `triage` does not create duplicates.

**Section C. Domain docs.** Default to **single-context**, with one `CONTEXT.md` and `docs/adr/` at the repo root. Write this layout without asking.

Offer **multi-context** only when exploration found monorepo signals. This layout uses a root `CONTEXT-MAP.md` that points to per-context `CONTEXT.md` files. Confirm which layout the user wants.

### 3. Confirm and edit

Show the user a draft of:

- The shared `## Agent skills` block to add to `AGENTS.md` and `CLAUDE.md`
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)

Let them edit before writing.

### 4. Write

**Edit both host instruction files:**

- Update `AGENTS.md` and `CLAUDE.md` when they exist.
- Create either file when it does not exist.
- Keep the `## Agent skills` block identical in both files.
- Preserve all content outside that block.

If an `## Agent skills` block exists, update it in place. Do not append a duplicate block.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### Wayfinder operations

[one-line summary of where wayfinder operations are tracked]. See `docs/agents/wayfinder-operations.md`.
```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md). GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md). GitLab issue tracker
- [issue-tracker-jira.md](./issue-tracker-jira.md). Jira issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md). Local-markdown issue tracker
- [triage-labels.md](./triage-labels.md). Label mapping (only if `triage` is installed)
- [domain.md](./domain.md). Domain doc consumer rules + layout
- [wayfinder-operations.md](./wayfinder-operations.md) - mandatory rules for the wayfinder skill

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later. Re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
