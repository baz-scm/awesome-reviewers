---
title: Stable Hit Target Styling
description: When styling CSS interactions and decorative frames, drive hover/focus
  state from stable container elements—not from children whose size/geometry changes.
  This prevents feedback loops (hover jitter) and makes components easier to compose.
repository: facebook/react#b11
label: Code Style
language: Css
comments_count: 2
repository_stars: 251894
---

When styling CSS interactions and decorative frames, drive hover/focus state from stable container elements—not from children whose size/geometry changes. This prevents feedback loops (hover jitter) and makes components easier to compose.

Apply:
- Put borders/frames on the container that owns the layout box. Avoid per-line borders on inner elements, and don’t duplicate borders if a parent already defines them.
- For hover/animation: keep the clickable “hit target” as the outer box/step, and animate/clamp the inner visuals. Use fixed height/line-height and `overflow: hidden` so animated content can’t pop outside the hit target.
- Ensure selectors target the stable element (e.g., parent/step) rather than the animating bead.

Example pattern:
```css
.container {
  height: 1.5rem;
  padding: 0.25rem;
  overflow: hidden; /* clamp animated inner visuals */
}

/* Stable hit target drives interaction */
.containerStep:hover .bead {
  /* animate the inner visual */
  height: 0.75rem;
}

/* Don’t attach hover to the shrinking/expanding child itself */
/* .bead:hover { ... } */
```

Use this rule to avoid jittery hover behavior and to keep visual framing consistent across composed components.