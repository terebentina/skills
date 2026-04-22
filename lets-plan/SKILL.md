---
name: lets-plan
description: >-
  Interview the user about a plan or design, resolving decisions one at a
  time until ready to implement. Make sure to use this whenever the user
  wants to create a plan, stress-test a plan, design a system, brainstorm
  architecture, or says "let's plan", "help me think through", "what should
  we consider", even without the word "plan".
---

1. Enter plan mode if not already in it.
2. Interview the user relentlessly about every aspect of this plan. 
3. Ask one question at a time via AskUserQuestion, always with a recommended answer. Integrate each answer before the next question.
4. Order questions by leverage: resolve the decision that most constrains downstream choices first, then re-evaluate.
5. If a question can be answered by exploring the codebase, explore the codebase instead.
6. Stop when no unresolved decisions would change the implementation, or remaining questions are cosmetic.
7. Write the plan in bullets. Minimal prose, skip filler, keep it extremely concise.
8. Before ExitPlanMode, you MUST run `/terebentina:fresh-eyes` (a review pass that helps catch bad assumptions). Address anything it surfaces — return to step 2 if it raises new questions. Do not exit plan mode until the review is clean.
