# Agent Skills

A collection of agent skills that extend capabilities across planning, development, and tooling.

## Installation

To install into claude code:

```
claude plugins marketplace add terebentina/skills
```

Alternatively, you can install individual skills one by one for multiple LLMs and tools with the commands in the following section.

## Planning & Design

These skills help you think through problems before writing code.

- **lets-plan** — Get relentlessly interviewed about a plan or design until every branch of the decision tree is resolved.

  ```
  npx skills@latest add terebentina/skills/lets-plan
  ```
- **fresh-eyes** — Review the plan with fresh eyes

  ```
  npx skills@latest add terebentina/skills/fresh-eyes
  ```
- **to-gh-prd** — Turn the current conversation context into a PRD and submit it as a GitHub issue. No interview — just synthesizes what you've already discussed.

  ```
  npx skills@latest add terebentina/skills/to-gh-prd
  ```

- **to-gh-issues** — Break any plan, spec, or PRD into independently-grabbable GitHub issues (parent + sub-issues) using vertical slices.

  ```
  npx skills@latest add terebentina/skills/to-gh-issues
  ```
  
### Thanks

Many thanks to [Matt Pocock](https://github.com/mattpocock) for his awesome teaching skills and always being an inspiration.
