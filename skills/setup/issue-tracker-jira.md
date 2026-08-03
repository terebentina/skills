# Issue tracker: Jira

Tickets and specs (epics) for this repo live as Jira issues. Use the [`jira`](https://github.com/ankitpokhrel/jira-cli) CLI for all operations.
Validate that the CLI has been installed by testing `jira` is accessible as a cli tool. 
Validate that the tool config exists (`~/.config/.jira/.config.yml` by default).
Ask the user to run `jira init` if not configured and stop.

Jira identifies issues by **issue key** (e.g. `PROJ-123`), not a numeric id. Wherever docs say `<number>`, pass the issue key instead.

## Conventions

- **Create a ticket**: `jira issue create -tTask -s "..." -b "..." --no-input`. The `-t`/`--type` flag is required and must match an issue type configured for the project (`Task`, `Story`, `Bug`, `Epic`, ...). For multi-line bodies, pipe via stdin: `echo "$body" | jira issue create -s "..." -tTask --no-input`, or use `--template -` to read from stdin.
- **Read a ticket**: `jira issue view <KEY> --comments 50`.
- **List tickets**: `jira issue list --raw` for JSON output (`--plain` for text, `--csv` for CSV). Filter with `-s "To Do"` (status), `-l <label>`, `-a $(jira me)` (assignee), or raw JQL via `-q "..."`. Note: status values are the project's actual workflow status names (e.g. `"To Do"`, `"In Progress"`, `Done`) — there is no equivalent of GitHub's universal `open`/`closed` states.
- **Comment on a ticket**: `jira issue comment add <KEY> "..."`. Add `--internal` for internal-only comments.
- **Apply / remove labels**: `jira issue edit <KEY> --label foo` to add; `jira issue edit <KEY> --label -foo` to remove (prefix `-`). Multiple `--label` flags can be repeated.
- **Close**: Jira closes via workflow transitions, not a dedicated close action. Use `jira issue move <KEY> "<Status>"` where `<Status>` is whatever your project's done state is (commonly `Done` or `Closed` — varies by workflow). Pass `--comment "..."` to transition-with-comment in one step.
- **Link a ticket to its epic/spec**: `jira issue edit <KEY> -P <PRD-key>`.
- **Link tickets and epics/specs**: `jira issue link <INWARD_ISSUE_KEY> <OUTWARD_ISSUE_KEY> <ISSUE_LINK_TYPE>`. Examples: `jira issue link APP-1 APP-2 Duplicate`, `jira issue link APP-1 APP-2 Block`

- The project key comes from `jira init`'s config file (`~/.config/.jira/.config.yml` by default) — not from `git remote`. There is no automatic git-host-to-Jira mapping.

## When a skill says "publish to the issue tracker"

Create a Jira ticket.

## When a skill says "fetch the relevant ticket"

Run `jira issue view <KEY> --comments 50`.

## Wayfinding operations

Used by `wayfinder`. The **map** is a single epic with **child** issues as tickets.

- **Map**: a single epic labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body.
- **Child ticket**: a ticket linked to the map as a sub-issue. Labels: `wayfinder:<type>` (`research`/`prototype`/`planning`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: Jira's **native issue dependencies** — the canonical, UI-visible representation. A ticket is unblocked when every blocker is closed.
- **Frontier query**: list the map's open children (scoped to the map's sub-issues / task list), drop any with an open blocker or an assignee; first in map order wins.
- **Claim**: Assign the issue to the user — the session's first write.
- **Resolve**: Comment on the ticket with the summary then close it, then append a context pointer to the map's Decisions-so-far.
