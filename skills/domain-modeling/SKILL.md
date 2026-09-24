---
name: domain-modeling
description: Use when the user wants to define or sharpen domain terminology, maintain a ubiquitous language in CONTEXT.md, or record an architectural decision.
---

# Domain modeling

Build and sharpen the project's domain model while you design. Challenge terms, test relationships with edge cases, and record each resolved term or decision.

Reading `CONTEXT.md` for project vocabulary is not domain modeling. Use this process only when the model changes.

Respect a calling skill's write boundary. When `wayfinder` calls this skill, read existing domain documents without updating `CONTEXT.md` or any ADR. Record proposed glossary changes and ADRs as implementation follow-ups under the active Wayfinder effort.

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create each file only when you have something to write. Create `CONTEXT.md` when the first term is resolved. Create `docs/adr/` when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "When you say 'account', do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When you discuss domain relationships, stress-test them with specific scenarios. Invent edge cases that force precise boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` immediately. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

Do not include implementation details in `CONTEXT.md`. It is a glossary, not a spec, scratch pad, or record of implementation decisions.

### Offer ADRs sparingly

Use [ADR-FORMAT.md](./ADR-FORMAT.md) to decide whether a decision needs an ADR and to write it.
