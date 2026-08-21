# Wayfinder operations

The `wayfinder` skill may create or modify files only under `.scratch/wayfinder/<effort>/`.

Treat all other paths as read-only. Do not create branches, worktrees, commits, issue-tracker changes, ADRs, or glossary updates.

Store each deferred project record in its source ticket. Link it from the map's **Implementation follow-ups** section.

The user later runs `to-spec`, `to-tickets`, and `implement`, in that order. Those skills perform the deferred work.

The **map** is a file with one **child** file per ticket.

## Wayfinder files and file types

- **Map**: `.scratch/wayfinder/<effort>/map.md`. The destination, notes, decisions, implementation follow-ups, fog, and scope.
- **Child ticket**: `.scratch/wayfinder/<effort>/tickets/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`planning`/`task`). A `Status:` line records `open`, `claimed`, or `resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/wayfinder/<effort>/tickets/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.
- **Defer**: add an `## Implementation follow-up` to the ticket. Link it from the map when implementation must create an ADR or another project record.
