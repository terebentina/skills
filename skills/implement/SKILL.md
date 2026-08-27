---
name: implement
description: Build ready-for-agent tickets from a spec, epic, or ticket ID. Use the ticket state and context regardless of who created it.
argument-hint: "<epic-id | ticket-id>"
disable-model-invocation: true
---

# Implement

You are the **orchestrator**. You do not write ticket code yourself. Dispatch one subagent for each ticket in the dependency **frontier**. Give each subagent an isolated worktree. Integrate one ticket at a time, verify the merged branch, and then recompute the frontier.

**Required methods** (include them in each subagent's brief, and use them yourself):
- Use the `domain-modeling` skill when domain terminology or project records change.
- Use test-driven development for each ticket.
- Use one isolated Git worktree for each subagent.
- Verify all required checks before you claim completion.
- Ask the user before you push, open a pull request, or merge.

Follow **the repo's tracker doc** for frontier queries, native blocking, claims, and closure. Run `setup` if the tracker doc is missing.

## 1. Explore

Read, don't assume:
- `CONTEXT.md` / `CONTEXT-MAP.md` and any ADRs in the area you're touching. Subagents must respect them.
- The tracker doc, for how this repo expresses ticket state, blocking, and frontier queries.
- The project's **test, lint, and typecheck commands** and its **branch naming convention** (infer from existing branches / CI config / CONTEXT.md). You need all four before dispatching anyone.

## 2. Resolve the argument

1. No argument → stop with a helpful error.
2. Resolve it against the tracker; confirm it names a real epic or ticket. If not in the tracker, check `.scratch/` for a local spec/ticket.
3. Unresolvable by either → stop with a helpful message.
4. Determine **epic or single ticket** per the tracker doc (epics have children/sub-issues).

## 3. Prepare

1. Ensure a **clean working tree** and a **green baseline**. The branch must start from committed work that passes test/lint/typecheck, since every post-merge re-verification is measured against it. If the tree is dirty or the baseline is red, stop and ask.
2. Create and switch to a branch named after the spec/ticket using the repo convention, based off the **current** branch. If the branch already exists, reuse it and resume (skip already-closed tickets). Ensure .env is inside the worktrees and you installed node_modules there. Don't just link node_modules as pnpm refuses that.
3. **Epic.** Collect children that are open and labelled `ready-for-agent`. Read their native blocking edges to build the dependency tree.
   - A ticket is **unblocked** when every ticket blocking it is closed.
   - Report a ready ticket blocked by an open ticket that lacks `ready-for-agent`. You cannot build that blocker, so the dependent cannot start.
4. **Single ticket.** Treat that ticket as the whole tree. If an open ticket blocks it, ask whether to build the blocker, proceed anyway, or wait.

## 4. Work the frontier (loop)

Repeat until no open `ready-for-agent` tickets remain:

1. **Compute the frontier**: open, `ready-for-agent`, unblocked tickets, in dependency order.
2. If the frontier is empty but open ready tickets remain, they are all blocked by unfinished or failed work → **stop and report**; do not spin.
3. Select the tickets to dispatch. Parallelize only siblings that touch **disjoint files**. When unsure, run one, merge it, and then dispatch the next. Cap parallel work at three tickets.
4. Before each dispatch, **claim** the ticket per the tracker doc. Assign it to `@me` and change its status to "in progress" so concurrent runs skip it.
5. Dispatch one subagent per selected ticket with the **brief** below and the right model for that ticket.
6. As each subagent returns, run the **merge protocol** below. Integrate one worktree at a time.
7. Recompute the frontier and continue. A completed ticket may unblock another ticket.

### Subagent brief

Each subagent receives:
- The ticket body and the epic's goal, plus the **summaries and cross-cutting decisions** returned by upstream and sibling tickets already merged. Parallel subagents cannot see each other's code, so these summaries are their coordination channel.
- Its worktree base: the **current spec-branch HEAD**.
- The rules: implement via TDD (write tests, watch them fail, implement, watch them pass); run lint + typecheck at the end and at a couple of checkpoints; respect ADRs and the domain glossary.
- What to return: its worktree branch name, a short summary of the work, findings relevant to downstream tickets, and **any decision it made that a sibling might contradict**.
- Any project record that the ticket must create. This list can include ADRs and glossary updates.

Create each required project record in the same ticket that first implements its decision. Use `domain-modeling` for ADR and glossary rules.

Do not alter an existing ADR unless the implementation ticket explicitly requires that change. Make each new ADR self-contained.

### Merge protocol

When several subagents return together, integrate them one at a time in dependency order (ties broken by return order).

1. If the spec-branch HEAD moved since the subagent branched, **rebase or refresh its worktree onto current HEAD first**. A merged sibling makes older worktrees stale and creates a common source of conflicts.
2. Merge into the spec branch and **squash to one commit per ticket** (not one commit for the whole epic), referencing the ticket id in the message.
3. **Re-run the project's tests, lint, and typecheck on the integrated spec branch.** Passing inside the worktree is not enough. Conflict resolution and integration can break things.
4. After the integrated branch passes, close the ticket per the tracker doc and clean up the worktree. If it goes **red**, revert the merge commit so the branch returns to its last green state. Then treat the ticket as a failure. A red spec branch invalidates every later merge check.

## When something fails

Behavior is conditional. Match the situation, don't improvise a resolution:

- **A subagent returns work that fails tests, lint, or typecheck.** Do not merge it. Re-dispatch once from the current HEAD in a fresh worktree, with the failure detail. If the retry fails, leave the ticket open and stop its branch of the tree. Keep merged work intact and report the failure.
- **The integrated branch fails verification after a merge.** Treat it exactly as above for that ticket. Do not close it or proceed into its dependents.
- **A ticket is unimplementable or conflicts with a sibling decision.** Do not choose an outcome. Show both options to the user and leave dependents blocked. A retry cannot resolve a decision conflict, even when the conflict causes a test failure.
- **You cannot confidently resolve a merge conflict.** Stop and surface it. Do not force a resolution that changes behavior.
- A failed ticket blocks its dependents. Leave them blocked, never build past a failure.

## Finish

When the frontier drains and every ready ticket is closed:
1. Confirm that the whole spec branch is green.
2. Ask the user whether to push, open a pull request, merge, or keep the branch local.
3. Do not push, open a pull request, or merge without the user's direction.
4. Report what landed and what did not (stopped or skipped tickets, and why).

If the run stops early with tickets still open, leave the spec branch intact with its landed commits. Report what landed and what is blocked, then offer to hand off the completed work. Never force a handoff. A later run skips closed tickets unless the user's ruling reopens one.

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

- **Merging without re-verifying the integrated branch.** Green in the worktree ≠ green after merge.
- **Merging two worktrees in parallel.** Serialize, and refresh stale worktrees onto the new HEAD first.
- **Squashing the whole epic into one commit.** One commit per ticket keeps history and revertability.
- **Plowing past a failed ticket into its dependents.** A failure gates everything downstream.
- **Inventing a resolution for a spec/sibling conflict.** That is the user's decision, not yours.
- **Unbounded fan-out.** Cap concurrency; more parallel worktrees on shared files means more conflicts, not more speed.
