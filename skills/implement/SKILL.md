---
name: implement
description: Use when building the tickets of a spec/epic, or a single ticket, from the repo's issue tracker — the code-writing step after planning and ticketing. Invoked with an epic or ticket id.
argument-hint: "<epic-id | ticket-id>"
disable-model-invocation: true
---

# Implement

You are the **orchestrator**. You do not write ticket code yourself. You drive the dependency **frontier** of a spec: dispatch one subagent per unblocked ticket into an isolated worktree, integrate each returned worktree back to the spec branch one commit at a time, **re-verify after every merge**, then recompute the frontier and repeat until it is empty.

**REQUIRED SUB-SKILLS** (name them in each subagent's brief, and use them yourself):
- **Write all prose in ASD-STE100 Simplified Technical English** — commit messages, code comments, subagent briefs, ticket comments, the PR body, and your messages to the user — via `/terebentina:domain-modeling`.
- Subagents implement via superpowers:test-driven-development.
- Worktree isolation via superpowers:using-git-worktrees.
- Before claiming any ticket or the epic complete, superpowers:verification-before-completion.
- Finish the branch via superpowers:finishing-a-development-branch.

All issue-tracker operations (frontier query, native blocking, claim, close) follow **the repo's tracker doc** — the same primitives the tracker doc documents for frontier/claim/blocking. The tracker should have been provided to you — run `/terebentina:setup` if not.

## 1. Explore

Read, don't assume:
- `CONTEXT.md` / `CONTEXT-MAP.md` and any ADRs in the area you're touching — subagents must respect them.
- The tracker doc, for how this repo expresses ticket state, blocking, and frontier queries.
- The project's **test, lint, and typecheck commands** and its **branch naming convention** (infer from existing branches / CI config / CONTEXT.md). You need all four before dispatching anyone.

## 2. Resolve the argument

1. No argument → stop with a helpful error.
2. Resolve it against the tracker; confirm it names a real epic or ticket. If not in the tracker, check `.scratch/` for a local spec/ticket.
3. Unresolvable by either → stop with a helpful message.
4. Determine **epic or single ticket** per the tracker doc (epics have children/sub-issues).

## 3. Prepare

1. Ensure a **clean working tree** and a **green baseline** — the branch must start from committed work that passes test/lint/typecheck, since every post-merge re-verification is measured against it. If the tree is dirty or the baseline is red, stop and ask.
2. Create and switch to a branch named after the spec/ticket using the repo convention, based off the **current** branch. If the branch already exists, reuse it and resume (skip already-closed tickets). Ensure any relevant but gitignored .env and node_modules are inside the worktrees.
3. **Epic:** collect children that are open AND labelled `ready-for-agent`, and read their native blocking edges to build the dependency tree. A ticket is **unblocked** when every ticket blocking it is closed (a closed blocker is satisfied; a blocker that lacks `ready-for-agent` is not something you will build — if it gates a ready ticket, that dependent can never start: report it, don't silently skip).
   **Single ticket:** the "tree" is that one ticket. If it is itself blocked by an open ticket, stop and ask the user how to proceed (build the blocker first / proceed anyway / wait) — do not guess.

## 4. Work the frontier (loop)

Repeat until no open `ready-for-agent` tickets remain:

1. **Compute the frontier**: open, `ready-for-agent`, unblocked tickets, in dependency order.
2. If the frontier is empty but open ready tickets remain, they are all blocked by unfinished or failed work → **stop and report**; do not spin.
3. **Dispatch** a subagent per frontier ticket. Use the right model for each ticket. Parallelize only siblings you are confident touch **disjoint files**; when unsure, serialize them (run one, merge it, dispatch the next) — parallel worktrees editing shared files multiply conflicts. Cap parallelism at ~3 even when disjoint. Before dispatching each, **claim** its ticket per the tracker doc (assign `@me`) and change the ticket status to "in progress" so concurrent runs skip it.
4. Give each subagent the **brief** below.
5. As each returns, run the **merge protocol** below — **serially**, one worktree at a time, never two merges at once.
6. Recompute the frontier (newly unblocked tickets appear) and continue.

### Subagent brief

Each subagent receives:
- The ticket body and the epic's goal, plus the **summaries and cross-cutting decisions** returned by upstream/sibling tickets already merged (parallel subagents cannot see each other's code — this prose is the only channel between them).
- Its worktree base: the **current spec-branch HEAD**.
- The rules: implement via TDD (write tests, watch them fail, implement, watch them pass); run lint + typecheck at the end and at a couple of checkpoints; respect ADRs and the domain glossary; write every comment, commit message, and returned summary in ASD-STE100 Simplified Technical English per `/terebentina:domain-modeling`.
- What to return: its worktree branch name, a short summary of the work, findings relevant to downstream tickets, and **any decision it made that a sibling might contradict**.

### Merge protocol

When several subagents return together, integrate them one at a time in dependency order (ties broken by return order).

1. If the spec-branch HEAD moved since the subagent branched, **rebase/refresh its worktree onto current HEAD first** (a merged sibling makes older worktrees stale — this is the common conflict source).
2. Merge into the spec branch and **squash to one commit per ticket** (not one commit for the whole epic), referencing the ticket id in the message.
3. **Re-run the project's tests, lint, and typecheck on the integrated spec branch.** Passing inside the worktree is not enough — conflict resolution and integration can break things.
4. Only when the integrated branch is green: close the ticket per the tracker doc and clean up the worktree. If it goes **red**, revert the merge commit so the branch returns to its last green state, then treat the ticket as a failure (below) — a red spec branch would poison every later merge's re-verification.

## When something fails

Behavior is conditional — match the situation, don't improvise a resolution:

- **Subagent can't make tests pass, returns broken/incomplete work, or lint/typecheck fails** (a transient or fixable failure): do not merge. Re-dispatch once into a **fresh worktree off current HEAD**, discarding the failed attempt, with the failure detail as context. Still failing → leave the ticket open, **stop that branch of the tree**, keep already-merged work intact, and report. Never merge red work; never fabricate a pass.
- **Integrated branch fails verification after a merge:** treat exactly as above for that ticket — do not close it, do not proceed into its dependents.
- **Ticket is unimplementable as written, or conflicts with a decision a sibling made:** do not pick a winner yourself. Stop, surface both options to the user, and leave dependents blocked pending their ruling. This governs even when the conflict is *why* the ticket's tests won't pass — a re-run can't resolve a decision, so route it here, not to the retry rule above.
- **Merge conflict you can't confidently resolve:** stop and surface it; don't force a resolution that changes behavior.
- A failed ticket blocks its dependents — leave them blocked, never build past a failure.

## Finish

When the frontier drains and every ready ticket is closed:
1. Confirm the whole spec branch is green (superpowers:verification-before-completion).
2. Hand off via superpowers:finishing-a-development-branch (push / PR / merge — the user's call). Do not push or open a PR unprompted.
3. Report what landed and what did not (stopped or skipped tickets, and why).

If the run instead stops early (a failure or a pending ruling) with tickets still open, leave the spec branch intact with its landed commits, report what landed and what is blocked, and *offer* — never force — handing off the completed work. A later resume skips closed tickets, unless the user's ruling reopens one.

## Stop conditions (quick reference)

| Situation | Action |
|---|---|
| No / unresolvable argument | Stop with a helpful message |
| Dirty working tree | Stop and ask |
| Single ticket is blocked | Ask the user how to proceed |
| Frontier empty but ready tickets remain | Stop and report (blocked graph / upstream failure) |
| Subagent fails twice | Leave ticket open, stop that branch, report |
| Ticket unimplementable / sibling conflict | Stop, surface to user, keep merged work |
| All ready tickets closed | Verify, hand off, report |

## Common mistakes

- **Merging without re-verifying the integrated branch** — green in the worktree ≠ green after merge.
- **Merging two worktrees in parallel** — serialize, and refresh stale worktrees onto the new HEAD first.
- **Squashing the whole epic into one commit** — one commit per ticket keeps history and revertability.
- **Plowing past a failed ticket into its dependents** — a failure gates everything downstream.
- **Inventing a resolution for a spec/sibling conflict** — that is the user's decision, not yours.
- **Unbounded fan-out** — cap concurrency; more parallel worktrees on shared files means more conflicts, not more speed.
