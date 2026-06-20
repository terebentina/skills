# Agent Skills

A collection of agent skills that extend capabilities across planning, development, and tooling.

## Installation

To install into claude code:

```
claude plugins marketplace add terebentina/skills
```

Or for any LLM:
```
npx skills@latest add terebentina/skills
```

## List of skills

- **lets-plan-code** — Get interviewed about a coding plan.
- **lets-plan** — Get interviewed about a plan.
- **fresh-eyes** — Review the plan with fresh eyes
- **deps-up** — Update dependencies to the latest major version

Imported from [Matt's skills](https://github.com/mattpocock/skills):
- **diagnose** - Disciplined diagnosis loop for hard bugs and performance regressions: reproduce → minimise → hypothesise → instrument → fix → regression-test.
- **improve-codebase-architecture** - Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/
- **to-issues** - Break any plan, spec, or PRD into independently-grabbable GitHub issues using vertical slices.
- **to-prd** - Turn the current conversation context into a PRD and submit it as a GitHub issue. No interview — just synthesizes what you've already discussed.

### Thanks

Many thanks to [Matt Pocock](https://github.com/mattpocock) for his awesome teaching skills and always being an inspiration.
