---
name: lets-plan
description: >-
  Interview the user relentlessly about a plan or design until reaching
  shared understanding, resolving each branch of the decision tree.
  Use when user wants to create a plan, stress-test a plan, design a
  system, brainstorm architecture, or asks "let's plan", "help me think
  through", or "what should we consider".
---

1. Switch to plan mode on invocation if not already in plan mode. 
2. Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.
3. Make the plan extremely concise. Sacrifice grammar for the sake of concision.
4. For each question, use AskUserQuestion and provide your recommended answer.
5. If a question can be answered by exploring the codebase, explore the codebase instead.
6. If the changes involve coding and programming languages then the plan should include unit tests and building each feature in TDD style: write the test first and run it and it should fail, write the implementation code, run the test again and it should pass. No need for integration tests.
7. MANDATORY: You MUST run `/fresh-eyes` before calling ExitPlanMode. Do not exit plan mode until the fresh-eyes review is complete and any issues found are addressed.
