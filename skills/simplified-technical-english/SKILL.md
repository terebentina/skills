---
name: simplified-technical-english
description: Use when writing any prose — code comments, commit and PR messages, ADRs, CONTEXT.md, specs, tickets, triage comments, plans, reports, research notes, subagent briefs, or replies to the user. Gives the ASD-STE100 Simplified Technical English rules that every other skill in this collection requires.
---

# Simplified Technical English

Write all prose in **ASD-STE100 Simplified Technical English (STE)**. STE is a controlled English standard with two parts: a dictionary of approved words, and a set of writing rules. It makes text unambiguous for readers, translators, and agents.

You do not have the STE dictionary here. Apply Part 2 as a discipline: choose the simplest common word for each meaning, then keep to that one word.

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

## Technical names and technical verbs

STE permits technical names and technical verbs. The domain fixes their meaning, so they do not break rule 1 or rule 2.

Treat these as technical names and use them exactly:

- The terms in the repo's `CONTEXT.md` glossary
- The `/terebentina:codebase-design` vocabulary — module, interface, depth, seam, adapter, leverage, locality
- The named concepts of these skills — tracer bullet, frontier, map, destination, agent brief
- Product, library, tool, and API names

Do not replace a technical name with a plainer word, and do not give it a synonym. A precise term beats a simple one.

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

Correct what fails. Then send the text.

## Common mistakes

- **Applying STE only to documents.** Chat replies and code comments are prose. They count.
- **Flattening a technical name.** "Seam" and "interface" stay. Simplify the words around them.
- **Rewriting quoted text.** A quotation keeps its original wording.
- **Trading one long sentence for one long fragment.** Split the sentence. Do not delete "that" or an article to reach 20 words.
- **Silent synonym drift.** "Ticket", "issue", and "item" in one document is three words for one meaning. Pick one.
