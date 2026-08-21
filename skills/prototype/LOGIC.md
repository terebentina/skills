# Logic prototype

A tiny interactive terminal app that lets the user drive a state model by hand. Use it for **business logic, state transitions, or data shapes** that need concrete cases before they can be judged.

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where the user wants to **press buttons and watch state change**.

If the question is "what should this look like?", use [UI.md](UI.md) instead.

## Process

### 1. State the question

Before writing code, name the state model and the question in one paragraph. Put it in the prototype's README or a top-of-file comment. Make the question explicit so it can be checked later, whether the user is present or returning AFK.

### 2. Pick the language

Use the host project's language. If the project has no runtime, as in a documentation repository, ask.

Match the project's existing conventions for tooling. Don't add a new package manager or runtime just for the prototype.

### 3. Isolate the logic in a portable module

Put the logic that answers the question behind a small, pure interface. Keep it portable enough to move into the real codebase. The TUI is throwaway.

The right shape depends on the question:

- **A pure reducer.** `(state, action) => state`. Good when actions are discrete events and state is a single value.
- **A state machine.** Explicit states and transitions. Good when "which actions are even legal right now" is part of the question.
- **A small set of pure functions** over a plain data type. Good when there is no implicit current state and each operation is a transformation.
- **A class or module with a clear method surface** when the logic genuinely owns ongoing internal state.

Pick the shape that fits the question, not the shape that is easiest to wire to a TUI. Keep it pure: no I/O, terminal code, or `console.log` control flow. The TUI imports and calls it. Nothing flows the other direction.

### 4. Build the smallest TUI that exposes the state

Build it as a **lightweight TUI**. On every tick, clear the screen (`console.clear()` / `print("\033[2J\033[H")` / equivalent) and re-render the whole frame. The user should always see one stable view, not an ever-growing scrollback.

Each frame has two parts, in this order:

1. **Current state**, pretty-printed and diff-friendly (one field per line, or formatted JSON). Use **bold** for field names or section headers and **dim** for less important context (timestamps, IDs, derived values). Native ANSI escape codes are fine. `\x1b[1m` bold, `\x1b[2m` dim, `\x1b[0m` reset. No need to pull in a styling library unless one is already in the project.
2. **Keyboard shortcuts**, listed at the bottom: `[a] add user  [d] delete user  [t] tick clock  [q] quit`. Bold either the key or its description, whichever reads clearly.

Behaviour:

1. **Initialise state.** A single in-memory object/struct. Render the first frame on start.
2. **Read one keystroke (or one line)** at a time, dispatch to a handler that mutates state.
3. **Re-render** the full frame after every action. Don't append, replace.
4. **Loop until quit.**

The whole frame should fit on one screen.

### 5. Make it runnable in one command

Add a script to the project's existing task runner (`package.json` scripts, `Makefile`, `justfile`, `pyproject.toml`). Give the user one command, such as `pnpm run <prototype-name>`, that does not require remembering a path.

If the host project has no task runner, just put the command at the top of the prototype's README.

### 6. Hand it over

Give the user the run command. Their unexpected results expose errors in the model or its assumptions. Add new actions when they help answer the question.

### 7. Capture the answer and the prototype

Once the prototype answers its question, capture the answer and prototype as [SKILL.md](SKILL.md) describes. Move the validated reducer, state machine, or functions into the real module. Keep the TUI shell on the throwaway branch as a primary source.

## Anti-patterns

- **Don't add tests.** A prototype that needs tests is no longer a prototype.
- **Don't wire it to the real database.** Use an in-memory store unless the question is specifically about persistence.
- **Don't generalise.** No "what if we wanted to support X later." The prototype answers one question.
- **Don't blur the logic and the TUI together.** If the reducer / state machine references `console.log`, prompts, or terminal escape codes, it's no longer portable. Keep the TUI as a thin shell over a pure module.
- **Don't ship the TUI shell into production.** The shell is optimised for being driven by hand from a terminal. The logic module behind it is the bit worth keeping.
