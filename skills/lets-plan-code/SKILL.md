---
name: lets-plan-code
description: >-
  Plan session that integrates with the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise.
argument-hint: "work description"
---

# Let's Plan Code

Run a planning session, using the `/terebentina:domain-modeling` skill.

<what-to-do>
1. Interview the user relentlessly about every aspect of this plan.
2. Ask one question at a time via AskUserQuestion. Integrate each answer before the next question.
3. Order questions by leverage: resolve the decision that most constrains downstream choices first, then re-evaluate.
4. If a question can be answered by exploring the codebase, explore the codebase instead.
5. Stop when no unresolved decisions would change the implementation, or remaining questions are cosmetic.
6. Write the plan in bullets. Minimal prose, skip filler, keep it extremely concise.
7. When the plan is complete you MUST run `/terebentina:fresh-eyes` (a review pass that helps catch bad assumptions). Integrate its findings into your plan — return to step 2 if it raises new questions.
8. Show a summary of how many questions I answered this session.
</what-to-do>

## Supporting information

- If `docs/agents/issue-tracker.md` is missing from this repository, run `/terebentina:setup` first.
- Use the `/terebentina:domain-modeling` skill to plan the domain model.
