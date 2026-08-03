---
name: domain-modeling
description: Use when writing any prose — code comments, commit and PR messages, ADRs, CONTEXT.md, specs, tickets, triage comments, plans, reports, research notes, subagent briefs, or replies to the user. Also use when the user wants to pin down domain terminology or a ubiquitous language, or to record an architectural decision. Gives the ASD-STE100 Simplified Technical English rules that every other skill in this collection requires.
---

# Domain Modeling

This skill owns the project's language. It does two jobs:

- **Write in STE** — the ASD-STE100 rules for every word of prose you write. This job applies to every session.
- **Build the model** — challenge and sharpen the project's terms, then record them in `CONTEXT.md` and the decisions behind them in ADRs. This job applies when you change the model.

The two jobs share one list of domain terms. `CONTEXT.md` holds that list, and it is the only file that defines a domain term. "Build the model" decides what goes in it. "Write in STE" keeps each entry exact.

---

# Write in STE

Write all prose in **ASD-STE100 Simplified Technical English (STE)**. STE is a controlled English standard. It has a dictionary of approved words and a set of writing rules. It makes text unambiguous for readers, translators, and agents.

You do not have the STE dictionary here. Apply the writing rules as a discipline: choose the simplest common word for each meaning, then keep to that one word.

## Scope

STE applies to every word of prose you write:

- Code comments, docstrings, and log messages
- Commit messages, PR titles, and PR bodies
- ADRs, `CONTEXT.md`, specs, tickets, triage comments, and handoff documents
- Reports, plans, research notes, and briefs for subagents
- Your messages to the user

**Pass the rule on.** When you dispatch a subagent that writes prose, name this skill in its brief.

## What STE does not change

Leave these as they are:

- Code, identifiers, types, and file paths
- Command names, flags, and command output
- Text you quote from the user, a source, or an existing file
- Error strings that must match a known value

STE governs prose you author. It is not a licence to rewrite a file you were only asked to read.

## Words

1. **One word, one meaning.** Pick the simplest correct word. Use that same word every time. Do not vary it for style.
2. **Use the plain word.** Write "use", not "utilise". Write "start", not "initiate". Write "about", not "approximately".
3. **Keep the articles.** Write "the module fails", not "module fails".
4. **Use three nouns together at most.** Break a longer cluster with a preposition. Change "ticket status update failure" to "a failure to update the status of the ticket".
5. **Do not use an -ing form as a verb.** Use the infinitive, the imperative, the simple present, or the simple past. Change "the test is failing" to "the test fails".
6. **Do not use slang, idioms, metaphors, or jargon.** Write "the change touches many files", not "the blast radius is large".
7. **Write an abbreviation in full at its first use.** Then use the short form.

## Sentences

8. **20 words maximum for an instruction. 25 words maximum for a description.**
9. **One instruction per sentence.** If a sentence holds two instructions, write two sentences.
10. **Use the active voice.** Write "the test catches the bug", not "the bug is caught by the test".
11. **Use the imperative for an instruction.** Write "Run the tests", not "the tests should be run".
12. **Use a simple tense** — simple present, simple past, or simple future.
13. **Start a sentence with its topic.** Keep the subject next to its verb.
14. **Do not drop a word to save space.** Keep "that" and "which". Write "confirm that the branch is green", not "confirm the branch is green".

## Structure

15. **Six sentences maximum per paragraph.** State the topic in the first sentence.
16. **Use a list for a procedure or for a set of conditions.**
17. **Put a warning before the step it applies to.** Write it as a command. State the hazard first.

## Technical names

STE permits technical names and technical verbs. A glossary fixes their meaning, so they do not break rule 1 or rule 2.

A word is a technical name only when a glossary defines it. Three glossaries can define one:

- **The repo's `CONTEXT.md`** — the project's domain terms. "Build the model" below maintains this file, and it is the only list of domain terms. A term's `_Avoid_` list names the synonyms that rule 1 forbids.
- **The glossary of a skill you run under.** The `codebase-design` glossary holds the architecture terms. A skill can also define its own named concepts in its own text.
- **Product, library, tool, and API names.**

Do not replace a technical name with a plainer word, and do not give it a synonym. A precise term beats a simple one.

**Never define a term outside its glossary.** When another document needs a term, name the glossary that owns it. A second definition goes stale, and then the two documents disagree.

A word that no glossary defines is ordinary prose. Rule 1 and rule 2 apply to it in full.

## Rewrites

| Not STE                                                           | STE                                                 |
|-------------------------------------------------------------------|-----------------------------------------------------|
| Having identified the root cause, the fix was applied.            | We found the root cause. Then we applied the fix.   |
| This will likely end up being a fairly heavy lift.                | This change needs a lot of work.                    |
| Don't forget to make sure the tests are passing before you merge. | Confirm that the tests pass. Then merge.            |
| The user data synchronisation retry configuration                 | The configuration for retries of the user data sync |
| It's worth noting that the endpoint is deprecated.                | The endpoint is deprecated.                         |
| Kick off the deploy once CI goes green.                           | Start the deploy after CI passes.                   |
| The module is currently being refactored by the team.             | The team refactors the module now.                  |

## Self-check

Read the text again before you send or save it:

- [ ] Is every sentence 20 words or fewer (25 for a description)?
- [ ] Is every sentence active and in a simple tense?
- [ ] Does each instruction have its own sentence?
- [ ] Did you use one word per meaning throughout?
- [ ] Did you keep every article, "that", and "which"?
- [ ] Is every noun cluster three nouns or fewer?
- [ ] Is every paragraph six sentences or fewer?
- [ ] Does a glossary define every technical name you used?

Correct what fails. Then send the text.

## Common mistakes

- **Applying STE only to documents.** Chat replies and code comments are prose. They count.
- **Flattening a technical name.** "Seam" and "interface" stay. Simplify the words around them.
- **Rewriting quoted text.** A quotation keeps its original wording.
- **Trading one long sentence for one long fragment.** Split the sentence. Do not delete "that" or an article to reach 20 words.
- **Silent synonym drift.** "Ticket", "issue", and "item" in one document is three words for one meaning. Pick one.
- **Inventing a technical name.** A term you coined in this session is not a technical name. Either add it to `CONTEXT.md` with the steps below, or write plain prose.

---

# Build the model

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this job — that's a one-line habit any skill can do. This job is for when you're changing the model, not just consuming it.)

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

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
