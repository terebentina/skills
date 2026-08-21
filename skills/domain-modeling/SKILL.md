---
name: domain-modeling
description: Use when the user wants to define or sharpen domain terminology, maintain a ubiquitous language in CONTEXT.md, or record an architectural decision. Applies ASD-STE100 Simplified Technical English only to direct conversation with the user while this skill runs.
---

# Domain modeling

This skill owns the project's domain language. It does two jobs:

- **Talk to the user in STE.** Apply ASD-STE100 to direct user conversation while this skill runs.
- **Build the model.** Challenge and sharpen the project's terms, then record them in `CONTEXT.md` and the decisions behind them in ADRs. This job applies when you change the model.

The two jobs share one list of domain terms. `CONTEXT.md` holds that list, and it is the only file that defines a domain term. "Build the model" decides what goes in it. "Talk to the user in STE" uses those terms in conversation.

---

# Talk to the user in STE

Write direct conversational replies to the user in **ASD-STE100 Simplified Technical English (STE)** while this skill runs. This includes status updates, questions, summaries, and final replies.

You do not have the STE dictionary here. Apply the writing rules as a discipline: choose the simplest common word for each meaning, then keep to that one word.

## Scope: user conversation only

Do not apply STE to saved artifacts. Do not apply STE to messages for agents or developers. This includes:

- Code comments, docstrings, log messages, product copy, and terminal text
- Commit messages, pull request titles, and pull request bodies
- ADRs, `CONTEXT.md`, specs, tickets, triage comments, and handoff documents
- Wayfinder maps, Wayfinder tickets, reports, plans, and research notes
- Briefs, instructions, summaries, or other messages for agents

Do not put an STE requirement in an agent brief.

An artifact does not become user conversation when you paste or preview it in a reply. Apply STE only to the surrounding conversation.

## What STE does not change in a reply

Leave these as they are:

- Code, identifiers, types, and file paths
- Command names, flags, and command output
- Text you quote from the user, a source, or an existing file
- Error strings that must match a known value

STE governs only the conversational prose that you author for the user.

## Caller write boundaries

A calling skill can restrict where this skill writes. Always apply the narrowest write boundary.

When `wayfinder` calls this skill, use STE only in direct replies to the user. Read existing domain documents, but do not update `CONTEXT.md` or any ADR.

Record each proposed glossary change or ADR as an implementation follow-up under the active Wayfinder effort.

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
12. **Use a simple tense.** Use simple present, simple past, or simple future.
13. **Start a sentence with its topic.** Keep the subject next to its verb.
14. **Do not drop a word to save space.** Keep "that" and "which". Write "confirm that the branch is green", not "confirm the branch is green".

## Structure

15. **Six sentences maximum per paragraph.** State the topic in the first sentence.
16. **Use a list for a procedure or for a set of conditions.**
17. **Put a warning before the step it applies to.** Write it as a command. State the hazard first.

## Technical names

STE permits technical names and technical verbs in user replies. A glossary fixes their meaning, so they do not break rule 1 or rule 2.

A word is a technical name only when a glossary defines it. Three glossaries can define one:

- **The repo's `CONTEXT.md`.** This file owns the project's domain terms. "Build the model" below maintains it. A term's `_Avoid_` list names the synonyms that rule 1 forbids.
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

Read each user reply again before you send it:

- [ ] Is every sentence 20 words or fewer (25 for a description)?
- [ ] Is every sentence active and in a simple tense?
- [ ] Does each instruction have its own sentence?
- [ ] Did you use one word per meaning throughout?
- [ ] Did you keep every article, "that", and "which"?
- [ ] Is every noun cluster three nouns or fewer?
- [ ] Is every paragraph six sentences or fewer?
- [ ] Does a glossary define every technical name you used?

Correct what fails. Then send the reply.

## Common mistakes

- **Applying STE to artifacts.** The rule applies only to direct user conversation. It does not apply to saved files or agent messages.
- **Passing STE to an agent.** Do not add this writing restriction to an agent brief or handoff.
- **Flattening a technical name.** "Seam" and "interface" stay. Simplify the words around them.
- **Rewriting quoted text.** A quotation keeps its original wording.
- **Trading one long sentence for one long fragment.** Split the sentence. Do not delete "that" or an article to reach 20 words.
- **Silent synonym drift.** "Ticket", "issue", and "item" in one document is three words for one meaning. Pick one.
- **Inventing a technical name.** A term you coined in this session is not a technical name. Either add it to `CONTEXT.md` with the steps below, or write plain prose.

---

# Build the model

Build and sharpen the project's domain model while you design. Challenge terms, test relationships with edge cases, and record each resolved term or decision.

Reading `CONTEXT.md` for project vocabulary is not domain modeling. Use this process only when the model changes.

The STE rule does not apply to domain records.

Skip all project file updates when a calling skill sets a narrower write boundary. Use that skill's deferred record process instead.

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
