---
name: wayfinder
description: Explore work that exceeds one agent session as local decision tickets. Use only when the user asks to create or continue a Wayfinder map. Persist all exploration output under `.scratch/wayfinder/<effort>/` and never change files elsewhere.
disable-model-invocation: true
---

A loose idea has arrived. The work is too large for one agent session, and the route to the **destination** is unclear. This skill records the exploration as a **shared map** in local Markdown files. It resolves **decision tickets**, not implementation tickets, until the route is clear.

The destination varies per effort, and its name shapes every ticket. The destination can be a spec or a decision that precedes planning. The map applies to any domain that fits this process.

## Exploration boundary

**Treat this boundary as absolute. Supporting skills and effort notes cannot override it.**

Wayfinder may create or modify files only under `.scratch/wayfinder/<effort>/`.

Treat all other filesystem paths as read-only. This rule includes source code, project documents, configuration, `CONTEXT.md`, and Architectural Decision Records (ADRs).

Do not create, modify, move, or delete an ADR. Do not create, modify, move, or delete `CONTEXT.md`.

Do not install dependencies. Do not run formatters, migrations, or other commands that can modify files outside the effort directory.

Do not create branches, worktrees, or commits. Do not modify the issue tracker or any external system.

Pass this boundary to every supporting skill and subagent. If a supporting process conflicts with this boundary, this boundary takes precedence.

Wayfinder stores the map at `.scratch/wayfinder/<effort>/map.md`.

Wayfinder stores each ticket at `.scratch/wayfinder/<effort>/tickets/NN-<slug>.md`.

Store research notes, prototypes, and other exploration assets under the same effort directory. Link each asset from its decision ticket.

The effort directory contains the complete exploration record. Delete that directory to remove the effort.

### Deferred project records

Wayfinder records project documentation work, but it never performs that work.

When a decision needs an ADR, add an implementation follow-up to the resolved ticket. Add a link to that follow-up in the map.

Use the same process when a decision needs a glossary update or conflicts with an existing ADR.

State what the later implementation must record and why. Do not draft the ADR outside the effort directory.

### Handoff sequence

Wayfinder stops after it completes the exploration record. It does not start a later workflow skill.

The user starts each later stage explicitly and in this order:

1. Use `to-spec` to turn the completed effort into a spec.
2. Use `to-tickets` after the user approves the spec.
3. Use `implement` after the user approves and publishes the tickets.

These later skills perform the project work that Wayfinder found. Wayfinder does not write a spec, implementation tickets, code, or project records.

## Plan, don't do

Wayfinder only explores. Each ticket resolves a decision, and the map is complete when no decision blocks the later workflow. Stop when the next action would implement the destination. Record that action as an implementation follow-up.

## Refer by name

Every map and ticket has a **name**. The name is its title. In narration and the map's **Decisions so far**, use that name instead of a bare number or slug. Use the file path as the link target when a link helps.

## The map

The map at `.scratch/wayfinder/<effort>/map.md` is the canonical artifact. Its tickets are child files in `.scratch/wayfinder/<effort>/tickets/`.

The map is an **index**, not a store. Each decision lives in its ticket. The map links to the ticket and gives only enough detail to judge whether the decision is relevant.

**The map, its child tickets, blocking, and frontier queries all live in local files.** Read `skills/setup/wayfinder-operations.md` for the file format.

### The map body

The whole map loads at low resolution once per session. Open tickets are **not** listed. Find them by scanning the effort's `tickets/` directory.

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link) — <one-line gist of the answer>

## Implementation follow-ups

<!-- deferred work for to-spec, to-tickets, and implement; link each item to the decision ticket that requires it -->

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket is a **child file** of the map. Its file name is its identity. Its body is the question, sized to one 100K token agent session:

```markdown
#<NN> — <ticket title>

Type: <research|prototype|planning|task>
Status: open
Blocked by: None

## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `Type:` line with one of `research`, `prototype`, `planning`, or `task` (see [Ticket Types](#ticket-types)).

A session **claims** a ticket by changing its `Status:` line to `claimed`, **first**, before any work, so concurrent sessions skip it. An open ticket with no claim is unclaimed.

Blocking uses a `Blocked by:` line that lists ticket numbers. A ticket is **unblocked** when every listed ticket has `Status: resolved`. The **frontier** is the open, unblocked, unclaimed edge of the known.

The answer is not part of the question body. Record it under `## Answer` when the ticket resolves. Link effort-local assets from the ticket.

If implementation must create an ADR or another project record, add this section:

```markdown
## Implementation follow-up

- Create <project record> during implementation because <reason>.
```

Add a link and a short gist to the map's **Implementation follow-ups** section.

## Ticket types

Every ticket is either **HITL** or **AFK**. A HITL ticket requires a live exchange with a human who speaks for themselves. An AFK ticket is driven by the agent alone. The agent never answers the human's side of a HITL exchange.

- **Research** (AFK): Read primary sources to find a fact that a decision needs. A `research` subagent resolves it. Store its report under the effort directory.
- **Prototype** (HITL): Create an effort-local artifact that makes a design question concrete. Use the `prototype` skill within the exploration boundary.
- **Planning** (HITL): Use `lets-plan-code` and `domain-modeling` to resolve one question with the user. Apply the exploration boundary to both skills.
- **Task** (HITL or AFK): Create an effort-local exploration artifact that unblocks a decision. Defer external actions and project changes to implementation.

## Fog of war

The map is _deliberately_ incomplete. Do not chart what you cannot yet see. The **fog of war** holds decisions and investigations that depend on open questions and cannot yet become tickets. Resolving a ticket clears part of the fog and may make the next ticket precise. Continue until the route to the destination is clear and no tickets remain.

The map's **Not yet specified** section holds in-scope questions that are not precise enough for tickets. Record what is known and what must be revisited. This section tells collaborators where the effort may go next.

**Fog or ticket?** The test is whether you can state the question precisely now, _not_ whether you can answer it now.

- **Ticket when** the question is already sharp, even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only gathers _toward_ the destination. Work beyond the destination is **out of scope**, not fog, and does not belong in **Not yet specified**. Record it in the map's **Out of scope** section.

Out-of-scope work never graduates because the frontier stops at the destination. If the destination changes to include that work, start a fresh effort.

Ruling something out of scope is not a step on the route. If an existing ticket sits beyond the destination, set its `Status:` to `resolved`. Add its gist and the reason to **Out of scope**. Do not add it to **Decisions so far**, which records the route actually taken.

## Invocation

Two modes. In either mode, **resolve no more than one ticket per session**, except research tickets.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Use `lets-plan-code` and `domain-modeling` within the exploration boundary. The destination fixes the scope.
2. **Map the frontier.** Plan breadth-first across the whole space. Find the open decisions and the first steps available now. If no fog remains, the route is already clear and one session can cover it. Stop and ask the user how to proceed without a map.
3. **Create the map** at `.scratch/wayfinder/<effort>/map.md`. Fill in Destination and Notes. Leave Decisions-so-far and Implementation follow-ups empty. Sketch the fog in **Not yet specified**.
4. **Create the tickets you can specify now** as child files in `.scratch/wayfinder/<effort>/tickets/`. Number them in dependency order. Add each `Blocked by:` line after all ticket files exist. Keep everything else in the fog under **Not yet specified**.
5. **Start the research subagents.** Start one subagent for each `research` ticket. Give each subagent the effort path and the exploration boundary. Do not create a branch or worktree.
6. Stop. Charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with an effort name. The effort name selects the map and the next frontier ticket.

1. Load `.scratch/wayfinder/<effort>/map.md` as the low-resolution view. Do not load every ticket body.
2. Choose the first frontier ticket in number order. Do not bypass the frontier because a ticket name or number is supplied. **Claim it** by writing `Status: claimed` before any work.
3. If no frontier ticket exists, inspect the fog and open tickets.
   - If `Not yet specified` is empty and every ticket is resolved, say exactly: `No fog remains, everything is ready.` Then stop.
   - If open tickets remain but none is in the frontier, report that the effort waits for a claim or blocker to clear, and stop.
   - If the fog contains an item that can now become a precise question, create the next ticket in the effort's `tickets/` directory, then continue with that ticket.
4. Resolve it. Read the full body of related tickets when needed. Apply the exploration boundary to every skill that the Notes block names.
5. Record the resolution. Append the answer under `## Answer`. Set `Status: resolved`. Add a context pointer to Decisions-so-far.
6. Record implementation follow-ups. Add them to the ticket and link them from the map. Include each required ADR or glossary update.
7. Add newly surfaced tickets. Graduate any fog that the answer makes precise. Remove each graduated item from **Not yet specified**. Store each new ticket in the effort's `tickets/` directory. If a ticket sits beyond the destination, rule it out of scope. If the decision invalidates another map file, update that effort-local file.

The user may run unblocked tickets in parallel, so expect other sessions to edit the effort's local files concurrently.

## End of the session

Show a summary of how many decisions the user made this session. List any implementation follow-ups. Do not start the handoff sequence.
