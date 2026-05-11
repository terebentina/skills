---
name: fresh-eyes
description: Re-read a draft plan with adversarial eyes before committing to it.
  Surfaces unstated assumptions, missing edge cases, scope creep, and
  decisions that conflict with earlier choices. Use before ExitPlanMode,
  or when user says "fresh eyes", "stress-test this", "what am I missing".
---

Re-read the plan as if you've never seen it. For each section, ask:

- **Unstated assumptions** — what is the plan taking for granted that isn't written down?
- **Missing edge cases** — what happens at empty/null/concurrent/failed boundaries?
- **Scope creep** — does any step solve a problem the user didn't ask about?
- **Internal contradictions** — does a later decision invalidate an earlier one?
- **Reversibility** — which steps are hard to undo, and is that called out?

Surface every concern as a short bullet. Don't fix them — just flag them.
