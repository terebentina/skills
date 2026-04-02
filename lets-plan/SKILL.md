---
name: lets-plan
description: >-
  Interview the user relentlessly about a plan or design until reaching
  shared understanding, resolving each branch of the decision tree.
  Use when user wants to create a plan, stress-test a plan, design a
  system, brainstorm architecture, or asks "let's plan", "help me think
  through", or "what should we consider".
---

- Switch to plan mode on invocation if not already in plan mode. 
- Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.
- Make the plan extremely concise. Sacrifice grammar for the sake of concision.
- For each question, use AskUserQuestion and provide your recommended answer.
- If a question can be answered by exploring the codebase, explore the codebase instead.
- If the changes involve coding and programming languages then the plan should include unit tests and building each feature in TDD style: write the test first and run it and it should fail, write the implementation code, run the test again and it should pass. No need for integration tests.
- MANDATORY: You MUST run `/fresh-eyes` before calling ExitPlanMode. Do not exit plan mode until the fresh-eyes review is complete and any issues found are addressed.
