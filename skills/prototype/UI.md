# UI prototype

Generate **several radically different UI variations** on a single route, switchable from a floating bottom bar. The user flips between variants in the browser, picks one (or steals bits from each), then throws the rest away.

If the question is about logic or state rather than appearance, use [LOGIC.md](LOGIC.md).

## When this is the right shape

- "What should this page look like?"
- "I want to see a few options for this dashboard before committing."
- "Try a different layout for the settings screen."
- Any time the user would otherwise spend a day picking between three vague mockups in their head.

## Two sub-shapes: prefer sub-shape A

A UI prototype is easier to judge inside the existing app, with its real header, sidebar, data, and density. An isolated route hides layout constraints. Default to sub-shape A when an existing page can host the variants. Use sub-shape B only when no nearby page fits.

### Sub-shape A: adjustment to an existing page (preferred)

The route already exists. Variants are rendered **on the same route**, gated by a `?variant=` URL search param. Keep the existing data fetching, params, and auth while swapping only the rendering. This is the default; pick it unless there's a specific reason not to.

If the prototype has no page yet but belongs inside an existing page, use sub-shape A. Examples include a dashboard section, a settings card, or a step in an existing flow. Mount the variants inside the host page.

### Sub-shape B: a new page (last resort)

Use this only when no existing page can host the prototype. Examples include a new top-level page or a flow that cannot fit inside an existing page.

Create a **throwaway route** with the project's routing convention. Do not invent a new top-level structure. Include `prototype` in the path or filename. Use the same `?variant=` pattern.

Before committing to sub-shape B, sanity-check: is there really no existing page this could be embedded in? An empty route hides design problems that a populated one would expose.

In both sub-shapes the floating bottom bar is identical.

## Process

### 1. State the question and pick N

Default to **3 variants**. More than 5 stops being radically different and starts being noise. Cap there.

Write down the plan in one line, in the prototype's location or a top-of-file comment:

> "Three variants of the settings page, switchable via `?variant=`, on the existing `/settings` route."

This works whether the user is here to push back or not.

### 2. Generate radically different variants

Draft each variant. Hold each one to:

- The page's purpose and the data it has access to.
- The project's component library / styling system (TailwindCSS, shadcn, MUI, plain CSS, whatever).
- A clear exported component name, such as `VariantA`, `VariantB`, or `VariantC`.

Variants must be **structurally different** in layout, information hierarchy, or primary action. Colour changes and small card-grid variations do not test a structural choice. If two drafts are too similar, redo one with explicit "do not use a card grid" guidance.

### 3. Wire them together

Create a single switcher component on the route:

```tsx
// pseudo-code — adapt to the project's framework
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A','B','C']} current={variant} />
  </>
);
```

For sub-shape A (existing page): keep all the existing data fetching above the switcher; only the rendered subtree changes per variant.

For sub-shape B (new page): the throwaway route under `/prototype/<name>` mounts the same switcher.

### 4. Build the floating switcher

A small fixed-position bar at the bottom-centre of the screen with three pieces:

- **Left arrow.** Cycles to the previous variant (wraps around).
- **Variant label.** Show the current variant key and its exported name, when present. For example, `B: Sidebar layout`.
- **Right arrow.** Cycles forward (wraps around).

Behaviour:

- Clicking an arrow updates the URL search param with the framework's router, such as `router.replace` on Next or `navigate` on React Router. This keeps the variant shareable and stable across reloads.
- Keyboard: `←` and `→` arrow keys also cycle. Don't intercept arrow keys when an `<input>`, `<textarea>`, or `[contenteditable]` is focused.
- Visually distinct from the page, with a high-contrast pill or subtle shadow, so it is not mistaken for part of the design.
- Hidden in production builds. Gate on `process.env.NODE_ENV !== 'production'` or an equivalent check, so a stray prototype merge can't ship the bar to users.

Put the switcher in a single shared component so both sub-shapes can reuse it. Locate it wherever shared UI lives in the project.

### 5. Hand it over

Show the URL and the `?variant=` keys. The most useful feedback often combines parts of several variants, such as **"I want the header from B with the sidebar from C"**.

### 6. Capture the answer and clean up

Once a variant wins, record which variant won and why. Capture the prototype as [SKILL.md](SKILL.md) describes. Fold the winner into the real code and move the other variants to the throwaway branch:

- **Sub-shape A.** Fold the winner into the existing page; drop the losing variants and the switcher from main.
- **Sub-shape B.** Promote the winning variant to a real route; drop the throwaway route and the switcher from main.

The full set of variants is the primary source, so it lands on the throwaway branch, not the bin. Variant components and the switcher left in the main branch rot fast and confuse the next reader.

## Anti-patterns

- **Variants that differ only in colour or copy.** That's a tweak, not a prototype. Real variants disagree about structure.
- **Sharing too much code between variants.** A shared `<Header>` is fine; a shared `<Layout>` defeats the point. Each variant should be free to throw out the layout.
- **Wiring variants to real mutations.** Read-only prototypes are fine. If a variant needs to mutate, point it at a stub. The question is "what should this look like", not "does the backend work".
- **Promoting the prototype directly to production.** The variant code was written under prototype constraints (no tests, minimal error handling). Rewrite it properly when you fold it in.
