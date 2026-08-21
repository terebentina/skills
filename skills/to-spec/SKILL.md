---
name: to-spec
description: Turn the conversation, plan, or completed Wayfinder effort into a spec in the issue tracker. Use only when the user asks for a spec.
disable-model-invocation: true
---

This skill turns the current conversation and codebase understanding into a spec (you may know this document as a PRD). Do NOT interview the user. Synthesize what you already know.

For a completed Wayfinder effort, this skill is the first handoff stage. Run it only when the user explicitly requests a spec.

The issue tracker and triage label vocabulary should have been provided to you. Run `setup` if not.

## Process

1. If the source is a Wayfinder effort, read its map, resolved tickets, linked notes, and exploration assets. Treat the effort as read-only. Stop if fog or unresolved tickets remain.

2. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

3. Sketch the seams where tests will exercise the feature. Prefer the highest existing seam that can cover the behavior. Add another seam only when one cannot provide enough coverage.

Check with the user that these seams match their expectations.

4. Carry every Wayfinder implementation follow-up into the spec. Put required ADRs and glossary updates under **Project records to create**.

5. Write the spec using the template below, then publish it to the project issue tracker as an epic, not as a regular issue.

<spec-template>

## Problem statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User stories

A numbered list of user stories. Cover every actor, behavior, edge case, failure mode, and constraint established in the source material.

Use this format:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

## Implementation decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

### Project records to create

List each ADR, glossary update, or other project record that implementation must create. Name its source Wayfinder decision.

Do not create these project records during `to-spec`.

Do NOT include specific file paths or code snippets. Code structure changes, so these details become stale.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Include only the parts that carry the decision, not a working demo.

## Testing decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Similar tests already in the codebase

## Out of scope

A description of the things that are out of scope for this spec.

## Further notes

Any further notes about the feature.

</spec-template>

After the user approves the spec, stop. The user invokes `to-tickets` for the next stage.
