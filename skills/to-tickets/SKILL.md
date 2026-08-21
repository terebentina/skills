---
name: to-tickets
description: Split a plan or spec into tracer-bullet tickets with blocking edges. Use only when the user asks to create tickets.
disable-model-invocation: true
---

# To tickets

Break a plan, spec, or conversation into **tracer-bullet tickets**. Each ticket is a vertical slice and declares the tickets that **block** it.

For a Wayfinder handoff, this skill is the second stage. Run it after the user approves the spec and requests implementation tickets.

The issue tracker and triage label vocabulary should have been provided to you. Run `setup` if not.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

Read the spec's **Project records to create** section. Keep each deferred record linked to its source decision.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>
- Each slice cuts a narrow but COMPLETE vertical path through every layer (schema, API, UI, tests), not a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first
</vertical-slice-rules>

Give each ticket its **blocking edges**, which are the tickets that must complete before it can start. A ticket with no blockers can start immediately.

Assign each deferred project record to the earliest ticket that implements its decision. Add its creation as the first acceptance criterion.

Do not create or modify the deferred project record during `to-tickets`.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change, such as renaming a column or retyping a shared symbol, whose callers cannot move in one green vertical slice.

Sequence a wide refactor as **expand–contract**:

1. **Expand.** Add the new form beside the old form so existing callers keep working.
2. **Migrate.** Move callers in batches, such as one package or directory per ticket. Every migration ticket is blocked by the expand ticket.
3. **Contract.** Delete the old form after every migration ticket finishes. The contract ticket is blocked by every migration ticket.

Each ticket must keep CI green. If no migration batch can do that alone, use a shared integration branch. Make all batches block one final integration and verification ticket.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title.** Short descriptive name
- **Blocked by.** Other tickets that must complete first, if any
- **What it delivers.** The end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct? Does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker `setup` configured. The tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below. One ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking / sub-issue relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. Apply the `ready-for-agent` triage label unless instructed otherwise. An approved ticket has enough detail for an agent to start.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Do NOT close or modify any parent issue.

<local-ticket-template>

# <NN>. <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work from the user's perspective, not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None. Can start immediately".

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work from the user's perspective, not a layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None. Can start immediately".

</issue-template>

In either form, avoid specific file paths or code snippets because they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Include only the parts that carry the decision, not a working demo.

After the user approves and publishes the tickets, stop. The user invokes `implement` for the next stage.
