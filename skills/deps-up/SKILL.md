---
name: deps-up
description: Update one or more npm packages to their latest version (even across majors) while respecting the package manager's minimumReleaseAge, then verify nothing broke against a baseline. Use when the user runs /deps-up with package names, or asks to upgrade/bump a dependency.
argument-hint: "<package name | all>"
---

# Deps Up

Update the requested package(s) to their latest version (across majors if needed), respecting the package manager's `minimumReleaseAge`, and prove nothing broke by comparing a before/after baseline AND inspecting the code against the actual package changes.

The package(s) to update are passed as arguments, e.g. `/terebentina:deps-up @apollo/client` or `/terebentina:deps-up react react-dom`.

## Process

Do the steps in order. Do not start updating until you have shown the changes and captured a baseline.

### 1. Show the relevant changes between versions (do this first, before anything else)

For each requested package:

- Read the current installed version (from the lockfile / `node_modules/<pkg>/package.json`, not just the range in `package.json`).
- Determine the latest version available, **respecting the package manager's `minimumReleaseAge`** — do not consider versions newer than that cooldown window. See [minimumReleaseAge](#respecting-minimumreleaseage).
- Fetch the relevant changes between the current and target version: release notes / CHANGELOG / migration guides. Prefer the GitHub releases or the repo's CHANGELOG over guessing.
- Present a concise, filtered list of **breaking changes, deprecations, and notable behavior changes** that are relevant to this codebase — not the full changelog dump.

Then stop and let the user see this before you change anything.

### 2. Establish a baseline

Before touching any dependency, run the project's full check suite and record the results:

- tests
- lint
- typecheck

Detect the actual commands from `package.json` scripts (e.g. `test`, `lint`, `typecheck`/`tsc`). Record pass/fail and the count of any pre-existing failures so the comparison after the update is honest. A pre-existing failure is not caused by the update.

### 3. Update the package(s)

Update only the requested package(s) to the target version from step 1, using the project's package manager (detect from the lockfile: `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm, `yarn.lock` → yarn, `bun.lock` → bun). Update the range in `package.json` to the new major where applicable.

### 4. Fix breaking changes in the code

Do **not** rely on tests alone to catch breakage. Using the breaking-change list from step 1:

- Find every usage of the package in the codebase (the changed/removed/renamed APIs specifically).
- Inspect each usage against the actual package changes and update the code to match the new version's API and behavior.
- Apply any required migration steps from the package's migration guide.

### 5. Re-run checks and compare to baseline

Run the same tests, lint, and typecheck commands from step 2. Compare against the baseline:

- New failures introduced by the update → keep fixing (back to step 4).
- Failures that already existed in the baseline → note them, but they are out of scope.

Report the before/after comparison clearly so it is obvious the update introduced no regressions.

## Respecting minimumReleaseAge

`minimumReleaseAge` is a cooldown that refuses to install package versions published more recently than a configured age — it protects against compromised fresh releases.

- **pnpm**: `minimumReleaseAge` in `.npmrc` / `pnpm-workspace.yaml`. `pnpm update --latest` and `pnpm outdated` honor it automatically.
- **bun**: `minimumReleaseAge` in `bunfig.toml`.
- **npm/yarn**: no native setting — if the project has none, treat the latest published version as the target, but mention that no cooldown was enforced.

When the package manager enforces it, let the tool pick the newest eligible version. When it does not, do not manually install a version newer than any configured cooldown.

## Notes

- If a requested package does not exist or is already at the latest eligible version, say so and skip it.
- If multiple packages are requested, handle them together (they may be peers, e.g. `react` + `react-dom`) but show per-package change lists.
