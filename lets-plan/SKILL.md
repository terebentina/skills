---
name: lets-plan
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to create a plan, stress-test a plan, or mentions planning.
---

- Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.
- Make the plan extremely concise. Sacrifice grammar for the sake of concision.
- For each question, use the question tool and provide your recommended answer.
- If a question can be answered by exploring the codebase, explore the codebase instead.
- After every change to a finalized plan, before asking the user if they are ready to code, run a review of the plan with fresh eyes. This will help broaden your understanding of the plan and codebase and help you catch any issues you might have missed previously.
- If the changes involve coding and programming languages then the plan should include unit tests and building each feature in TDD style: write the test first and run it and it should fail, write the implementation code, run the test again and it should pass.
