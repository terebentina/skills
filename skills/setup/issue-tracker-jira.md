# Issue tracker: Jira

Tickets and specs (epics) for this repo live as Jira issues. Use the [`jira`](https://github.com/ankitpokhrel/jira-cli) CLI for all operations.
Confirm that the `jira` command is available.
Confirm that its config exists at `~/.config/.jira/.config.yml` or the configured path.
Ask the user to run `jira init` if not configured and stop.

Jira identifies issues by **issue key**, for example, `PROJ-123`, not a numeric ID. Wherever docs say `<number>`, pass the issue key instead.

## Conventions

- **Create a ticket**: `jira issue create -tTask -s "..." -b "..." --no-input`. The `-t`/`--type` flag is required and must match an issue type configured for the project (`Task`, `Story`, `Bug`, `Epic`, ...). For multi-line bodies, pipe via stdin: `echo "$body" | jira issue create -s "..." -tTask --no-input`, or use `--template -` to read from stdin.
- **Read a ticket**: `jira issue view <KEY> --comments 50`.
- **List tickets**: use `jira issue list --raw` for JSON, `--plain` for text, or `--csv` for CSV.
  - Filter by status with `-s "To Do"`, by label with `-l <label>`, or by assignee with `-a $(jira me)`.
  - Pass raw Jira Query Language with `-q "..."`.
  - Use the project's workflow status names, such as `"To Do"`, `"In Progress"`, or `Done`. Jira has no universal `open` and `closed` states.
- **Comment on a ticket**: `jira issue comment add <KEY> "..."`. Add `--internal` for internal-only comments.
- **Apply / remove labels**: `jira issue edit <KEY> --label foo` to add; `jira issue edit <KEY> --label -foo` to remove (prefix `-`). Multiple `--label` flags can be repeated.
- **Close**: Jira closes via workflow transitions, not a dedicated close action. Use `jira issue move <KEY> "<Status>"`, where `<Status>` is the project's done state, commonly `Done` or `Closed`. Pass `--comment "..."` to transition with a comment in one step.
- **Link a ticket to its epic/spec**: `jira issue edit <KEY> -P <PRD-key>`.
- **Link tickets and epics**: `jira issue link <INWARD_ISSUE_KEY> <OUTWARD_ISSUE_KEY> <ISSUE_LINK_TYPE>`. Examples: `jira issue link APP-1 APP-2 Duplicate`, `jira issue link APP-1 APP-2 Block`

- The project key comes from `jira init`'s config file (`~/.config/.jira/.config.yml` by default), not from `git remote`. There is no automatic git-host-to-Jira mapping.

## When a skill says "publish to the issue tracker"

Create a Jira ticket.

## When a skill says "fetch the relevant ticket"

Run `jira issue view <KEY> --comments 50`.
