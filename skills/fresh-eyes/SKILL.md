---
name: fresh-eyes
description: Re-read a draft plan with adversarial eyes before committing to it.
  Surfaces unstated assumptions, missing edge cases, scope creep, and
  decisions that conflict with earlier choices. Use before finalizing a plan,
  or when user says "fresh eyes", "stress-test this", "what am I missing".
---

Re-read the plan as if you've never seen it. For each section, ask:

- **Unstated assumptions.** What is the plan taking for granted that isn't written down?
- **Missing edge cases.** What happens at empty/null/concurrent/failed boundaries?
- **Scope creep.** Does any step solve a problem the user didn't ask about?
- **Internal contradictions.** Does a later decision invalidate an earlier one?

Surface every concern as a short bullet. Do not fix it. Verify each concern before you report it.
Check the relevant files, documentation, versions, or history when evidence can settle the concern.
Omit anything that the evidence rules out.
