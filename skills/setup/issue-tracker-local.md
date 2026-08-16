# Issue tracker: Local Markdown

Issues and specs (you may know a spec as a PRD) for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` — never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Wayfinding operations

Wayfinder uses a local map with one child file per ticket.

Wayfinder may write only under `.scratch/wayfinder/<effort>/`. It must not modify an issue, ADR, glossary, source file, branch, worktree, or commit.

Wayfinder records deferred project work in its local tickets and map. The user later runs `to-spec`, `to-tickets`, and `implement`, in that order.

- **Map**: `.scratch/wayfinder/<effort>/map.md` — the destination, notes, decisions, implementation follow-ups, fog, and scope.
- **Child ticket**: `.scratch/wayfinder/<effort>/tickets/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`planning`/`task`). A `Status:` line records `open`, `claimed`, or `resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/wayfinder/<effort>/tickets/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.
- **Defer**: add an `## Implementation follow-up` to the ticket. Link it from the map when implementation must create an ADR or another project record.
