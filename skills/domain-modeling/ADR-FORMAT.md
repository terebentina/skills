# ADR format

ADRs live in `docs/adr/` and use sequential names such as `0001-slug.md` and `0002-slug.md`.

Create the `docs/adr/` directory only when the first ADR is needed.

Write for an agent or developer who reads the ADR years later without the original context. Make the decision and its reason unambiguous.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. Its value comes from recording the decision and its reason, not from filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status frontmatter.** Use `proposed | accepted | deprecated | superseded by ADR-NNNN` when decisions are revisited
- **Considered Options.** Only when the rejected alternatives are worth remembering
- **Consequences.** Only when non-obvious downstream effects need to be called out

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse.** The cost of changing your mind later is meaningful
2. **Surprising without context.** A future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off.** There were genuine alternatives and you picked one for specific reasons

Skip decisions that are easy to reverse. If a decision is unsurprising, nobody will wonder why. If there was no real alternative, there is nothing to record.

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Record a database, message bus, auth provider, deployment target, or library that would take a quarter to replace.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it. Otherwise someone will suggest GraphQL again in six months.
