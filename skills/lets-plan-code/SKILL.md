---
name: lets-plan-code
description: >-
  Plan session that integrates with the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise.
---

# Let's Plan Code

Run a planning session, using the `domain-modeling` skill.

**Write all prose in ASD-STE100 Simplified Technical English** — the plan bullets, your questions, the `CONTEXT.md` and ADR updates, and your messages to the user. The `domain-modeling` skill above gives the rules.

## Wayfinder use

When `wayfinder` calls this skill, apply the active effort's exploration boundary.

Write only under `.scratch/wayfinder/<effort>/`. Do not modify `CONTEXT.md`, ADRs, source files, issue trackers, branches, worktrees, or commits.

Record a required glossary update or ADR as an implementation follow-up in the active Wayfinder ticket and map.

Return the plan to Wayfinder for storage. Do not create a separate project plan.

<what-to-do>
1. Interview the user relentlessly about every aspect of this plan.
2. Ask one concise question at a time. Use the host's user-input tool when it is available.
3. Order questions by leverage: resolve the decision that most constrains downstream choices first, then re-evaluate.
4. If a question can be answered by exploring the codebase, explore the codebase instead.
5. Stop when no unresolved decisions would change the implementation, or remaining questions are cosmetic.
6. Write the plan in bullets. Minimal prose, skip filler, keep it extremely concise.
7. When the plan is complete you MUST run `fresh-eyes` (a review pass that helps catch bad assumptions). Integrate its findings into your plan — return to step 2 if it raises new questions.
8. Show a summary of how many decisions I made this session.
</what-to-do>

## Supporting information

- If `docs/agents/issue-tracker.md` is missing from this repository, run `setup` first.
- Use the `domain-modeling` skill to plan the domain model.
