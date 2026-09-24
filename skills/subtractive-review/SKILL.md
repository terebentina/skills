---
name: subtractive-review
description: Review a codebase for safe deletions by pairing each removal with the invariant and evidence that make it safe.
disable-model-invocation: true
---

# Subtractive Review

Find code the repository no longer needs.

A finding is not a smell or a complexity score. It is one specific deletion,
plus the invariant that makes the deletion safe, plus evidence that the
invariant holds. If the invariant depends on unwritten domain knowledge, turn
it into a concrete question for the human instead of guessing.

This is a read-only review until the human approves particular removals.

## Process

### 1. Establish the contract

Read the repository instructions, domain documentation, tests, and current
working-tree state. Identify the supported callers and inputs for the area
under review. Record the command that currently verifies the repository, or
state that no usable baseline exists.

The user may name a file, module, or subsystem as the review scope. Search the
whole repository when establishing reachability. A local search cannot prove
that code has no callers elsewhere in the repository.

Treat an exported or documented public interface as having unknown external
callers unless the repository's compatibility policy says it can be removed.

### 2. Build a candidate list

Use the repository's existing analysis tools when available: symbol references,
call graphs, coverage, complexity reports, linters, or dead-code detectors. Do
not add a dependency just to run this review. Metrics and tool warnings choose
where to read; they are not findings and have no target value.

Look for:

- branches whose callers cannot produce the tested state;
- optional parameters or modes that every caller uses the same way;
- compatibility paths with no supported producer or consumer;
- errors converted into `null`, sentinels, or empty results that force every
  caller to branch;
- the same validation repeated after a constructor or boundary already
  establishes the invariant;
- private helpers with no real caller, one caller, or only test callers;
- abstractions introduced for hypothetical variation that never arrived.

One caller is a prompt to read, not a reason to inline. A helper earns its name
when the name communicates more than the body or when it contains a meaningful
concept. Complexity and line count cannot answer that question.

### 3. Prove each candidate

Trace every candidate through production entry points, scripts, tests,
configuration, generated code, reflection, registration, and dynamic dispatch
where the language permits them. Search for string references as well as direct
calls before treating a symbol as unused.

Classify it:

- **Ready to remove**: repository evidence or an already-documented invariant
  proves the path is unsupported or unreachable.
- **Question for the human**: one concrete domain fact would decide it.
- **Keep**: a real caller, supported input, compatibility promise, or clearer
  concept earns the code its place.

A test proves that code behaves as written. It does not prove that the tested
case belongs to the domain. When a test is the only evidence for a supposedly
supported case, ask whether the case is real.

Prefer invariants that the implementation can enforce. In order: make the
invalid state unrepresentable, assert it once at the input boundary, then
document it. Do not scatter the same check through downstream callers.

### 4. Report and stop

Start with the baseline, review scope, and stopping point. Then report each
ready removal with:

- **Where**: file and symbol;
- **Delete**: the exact branch, parameter, helper, or compatibility path;
- **Invariant**: the fact that makes deletion safe and where it is enforced;
- **Evidence**: callers, repository documentation, runtime contract, or a
  human-confirmed fact;
- **Verify**: the focused check that would catch a wrong deletion.

List unresolved questions separately in an answerable form, such as "Can
`parseOrder()` receive an empty item list?" Report any part of the requested
scope you did not reach.

Do not assign a score, severity, or percentage of complexity to remove. Stop
after the report and ask which removals the human approves.

### 5. Apply approved removals

Only after approval, apply one logically independent removal at a time. Remove
tests whose only purpose was to certify an excluded case, but preserve tests of
supported behaviour. Run the focused check after each removal and the full
baseline at the end. Inspect the final diff for unrelated changes and state any
remaining uncertainty.

Do not replace deleted code with a new abstraction. Do not commit unless the
human asks.

## Boundaries

- Use `code-review` for defects or conformance in a diff.
- Use `improve-codebase-architecture` for additive or restructuring proposals.
- Mention a bug discovered in passing, but leave it outside this report.
