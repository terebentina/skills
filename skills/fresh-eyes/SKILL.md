---
name: fresh-eyes
description: Re-read a draft plan with adversarial eyes before committing to it.
  Surfaces unstated assumptions, missing edge cases, scope creep, and
  decisions that conflict with earlier choices. Use before finalizing a plan,
  or when user says "fresh eyes", "stress-test this", "what am I missing".
---

**Write all prose in ASD-STE100 Simplified Technical English** — every concern you surface, and your messages to the user. **REQUIRED SUB-SKILL:** `domain-modeling`.

Re-read the plan as if you've never seen it. For each section, ask:

- **Unstated assumptions** — what is the plan taking for granted that isn't written down?
- **Missing edge cases** — what happens at empty/null/concurrent/failed boundaries? 
- **Scope creep** — does any step solve a problem the user didn't ask about?
- **Internal contradictions** — does a later decision invalidate an earlier one?

Surface every concern as a short bullet. Don't fix them — just flag them. For every concern, you must try to validate it's a valid concern. 
If they require you to check a file, documentation, a package version, changelog history, etc, you must do and validate it's a real concern before presenting your findings.
If a concern is proven to be a non-issue after exploring, then don't mention it at all in the list of findings.
