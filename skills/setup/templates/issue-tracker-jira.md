# Issue tracker: Jira

Issues and PRDs for this repo live as Jira issues. Use the [`jira`](https://github.com/ankitpokhrel/jira-cli) CLI for all operations. Assumes `jira init` has already been run (server URL, project key, and auth token are configured).

Jira identifies issues by **issue key** (e.g. `PROJ-123`), not a numeric id. Wherever docs say `<number>`, pass the issue key instead.

## Conventions

- **Create an issue**: `jira issue create -tTask -s "..." -b "..." --no-input`. The `-t`/`--type` flag is required and must match an issue type configured for the project (`Task`, `Story`, `Bug`, `Epic`, ...). For multi-line bodies, pipe via stdin: `echo "$body" | jira issue create -s "..." -tTask --no-input`, or use `--template -` to read from stdin.
- **Read an issue**: `jira issue view <KEY> --comments 50`.
- **List issues**: `jira issue list --raw` for JSON output (`--plain` for text, `--csv` for CSV). Filter with `-s "To Do"` (status), `-l <label>`, `-a $(jira me)` (assignee), or raw JQL via `-q "..."`. Note: status values are the project's actual workflow status names (e.g. `"To Do"`, `"In Progress"`, `Done`) — there is no equivalent of GitHub's universal `open`/`closed` states.
- **Comment on an issue**: `jira issue comment add <KEY> "..."`. Add `--internal` for internal-only comments.
- **Apply / remove labels**: `jira issue edit <KEY> --label foo` to add; `jira issue edit <KEY> --label -foo` to remove (prefix `-`). Multiple `--label` flags can be repeated.
- **Close**: Jira closes via workflow transitions, not a dedicated close action. Use `jira issue move <KEY> "<Status>"` where `<Status>` is whatever your project's done state is (commonly `Done` or `Closed` — varies by workflow). Pass `--comment "..."` to transition-with-comment in one step.

The project key comes from `jira init`'s config file (`~/.config/.jira/.config.yml` by default) — not from `git remote`. There is no automatic git-host-to-Jira mapping.

## Triage

**In Jira, prefer mapping the triage roles onto workflow statuses rather than free-form labels.** Jira already has a native state machine, and using statuses keeps issues visible in board columns instead of buried in label filters. Set the role values in `triage-labels.md` to your project's status names, and the triage skill should use `jira issue move <KEY> "<Status>"` instead of `jira issue edit --label`.

## When a skill says "publish to the issue tracker"

Create a Jira issue.

## When a skill says "fetch the relevant ticket"

Run `jira issue view <KEY> --comments 50`.
