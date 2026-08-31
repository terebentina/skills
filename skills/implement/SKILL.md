---
name: implement
description: Build ready-for-agent tickets from a spec, epic, or ticket ID. Use the ticket state and context regardless of who created it.
argument-hint: "<epic-id | ticket-id>"
disable-model-invocation: true
---

# Implement

Act only as the **orchestrator**; subagents write the ticket code. Work the dependency **frontier** in isolated worktrees, integrate one ticket at a time, verify the result, and recompute the frontier.

Follow the repo's tracker doc for queries, native blocking, claims, and closure. Run `terebentina:setup` if it is missing. Both orchestrator and subagents use `domain-modeling` whenever domain terminology or project records change.

Both the orchestrator and every subagent must read and obey all applicable `CODING_STANDARDS.md` rules. Include this requirement in every subagent brief.

## Prepare

1. Require an argument. Resolve it in the tracker, then `.scratch/`; stop with a helpful message if neither contains it. Treat tracker items with children as epics and other items as single tickets.
2. Read the applicable `CONTEXT.md` / `CONTEXT-MAP.md`, ADRs, tracker doc, branch convention, and test, lint, and typecheck commands.
3. Require a clean working tree and a committed baseline that passes all three checks. Otherwise stop and ask the user.
4. Create or resume a spec/ticket branch from the current branch using the repo convention. Skip tickets already closed. Provision each worktree with its required local config and dependencies; with pnpm, install `node_modules` rather than symlinking it.
5. Before the first commit or merge, get user approval that covers the intended operations. Also ask before pushing, opening a pull request, or merging the completed branch unless already authorized.
6. For an epic, build the graph from its open `ready-for-agent` children and their native blocking edges. A ticket is unblocked only when every blocker is closed. Report any ready ticket blocked by an open, non-ready ticket; do not build past it.
7. For a single ticket, treat it as the whole graph. If it has an open blocker, ask whether to build the blocker, proceed anyway, or wait.

## Work the frontier

Repeat while open `ready-for-agent` tickets remain:

1. Compute the frontier: open, ready tickets whose blockers are closed, in dependency order. If it is empty, stop and report the blocked graph.
2. Select at most three sibling tickets, and parallelize only when they touch disjoint files. When unsure, dispatch one.
3. Claim each selected ticket per the tracker doc: assign it to `@me` and move it to "in progress."
4. Dispatch one subagent per ticket with the brief below.
5. Integrate returned worktrees one at a time with the merge protocol, then recompute the frontier.

### Subagent brief

Each subagent receives:

- The ticket body, epic goal, current spec-branch HEAD, and summaries or cross-cutting decisions from already merged tickets. These summaries coordinate agents that cannot see parallel work.
- The assigned worktree and the repo's verification commands.
- The rules: use TDD (failing test, implementation, passing test); run lint and typecheck at checkpoints and at the end; respect the domain glossary and ADRs; complete any project record assigned to the ticket. Change an existing ADR only when the ticket requires it.
- The required return: branch name, work summary, downstream findings, and any decision a sibling might contradict.

### Merge protocol

Integrate in dependency order, breaking ties by return order:

1. If the spec-branch HEAD moved, rebase or refresh the worktree onto current HEAD.
2. Merge into the spec branch as one squashed commit per ticket, with the ticket ID in the message.
3. Re-run tests, lint, and typecheck on the integrated branch. Worktree results are insufficient.
4. On success, close the ticket per the tracker doc and remove its worktree.
5. On failure before merge, do not merge. On failure after merge, revert the merge so the spec branch returns to green. Retry the ticket once from current HEAD in a fresh worktree with the failure details. If it fails again, leave it open, report it, and stop its dependent branch.

Do not resolve an unimplementable ticket, contradictory sibling decisions, or an uncertain merge conflict by guessing. Show the options to the user and leave dependents blocked. Never build past failed work.

## Finish

When all ready tickets are closed, confirm the full branch is green and run `terebentina:code-review` against its starting point before claiming completion. Report landed, stopped, and skipped tickets, then ask whether to push, open a pull request, merge, or keep the branch local.

If work stops early, keep successful commits and report what landed and what remains blocked. Use `terebentina:handoff` only if the user asks for a handoff. A later run skips closed tickets unless the user's decision reopens one.
