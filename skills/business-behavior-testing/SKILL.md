---
name: business-behavior-testing
description: Select and write risk-based behavior tests for features or bug fixes. Use when deciding what to test, where to test it, or whether an agent-written test is worth keeping.
---

# Business behavior testing

Protect consequential behavior, not implementation steps. BDD-style scenarios may help name a rule; Gherkin and a red-green cycle are not requirements.

## Select scenarios

1. Read the ticket/spec, relevant domain vocabulary, and existing tests. State the user or business outcome being changed and a plausible regression that would matter (including money, access, data loss, or an important workflow). Check whether existing tests already catch it.
2. Keep a scenario only if it distinguishes correct behavior from that regression through an observable result. Cover the normal outcome and materially different rules or transitions when their failure matters. No test quota: one scenario can suffice; a risky rule can need several; if existing coverage suffices, add none.
3. Choose the narrowest **public seam** that exercises the real rule and its necessary collaborators: a domain/service API, command, or request boundary. Use the real business logic; control only external I/O, clock, or nondeterminism. Go end-to-end when the risk is in the wiring across boundaries, not by default.
4. Assert independently known outcomes from the spec or a worked example. For example, a discount-precedence test asserts the final payable amount for an eligible cart, not that `applyDiscount` was called. Name tests for the rule and outcome, not the method or branch.
5. If a bug has a suitable seam, observe the regression test fail before fixing it, then pass afterward. For a feature, write a test when it protects a selected scenario; implementation can precede a test when discovery makes the rule clearer. In every case, exercise the changed path and run the relevant existing tests.

## Keep or delete

A test earns its place when a plausible harmful change makes it fail while a behavior-preserving refactor leaves it green. Prefer existing coverage over duplicates. Remove tests that assert mocks echo inputs, private calls, copies, incidental defaults, wording, or code structure; use a throwaway smoke check instead when a permanent test would add no protection. Do not weaken coverage of consequential security, financial, or data-integrity rules to meet a test count.

Report the chosen seam, protected rule(s), and verification evidence. If no new test is warranted, say what existing coverage or smoke check protects the change.
