---
title: Stable Container Styling
description: When writing CSS for components, apply container-level styling (layout/borders
  and interaction hit targets) so behavior stays predictable and composes cleanly.
repository: facebook/react#b13
label: Code Style
language: Css
comments_count: 2
repository_stars: 251893
---

When writing CSS for components, apply container-level styling (layout/borders and interaction hit targets) so behavior stays predictable and composes cleanly.

Guidelines:
1) Put borders/layout primitives on the full container, not on a single-line/inner element.
   - This avoids borders that only cover part of the content and prevents duplicated borders when parents also style borders.
2) For interactive hover/focus states, ensure the hover selector is on the stable hit target (outer box/step), not on the animated child.
3) Keep interactive geometry stable:
   - Use fixed dimensions/line-height for the animating region.
   - Clip overflow so the animated element can’t visually “escape” the hit target.
   - Avoid hover animations that shrink/expand in a way that toggles hover repeatedly (“hover jitter loops”).

Example pattern:
```css
/* Stable hit target */
.ScrubberStep {
  position: relative;
  flex: 1;
  height: 1.5rem; /* fixed container height */
  display: flex;
  align-items: center;
  overflow: hidden; /* clip any inner animation */
}

/* Animate inner only */
.ScrubberBead {
  height: 0.5rem;
  width: 100%;
  transition: height 0.2s ease;
}

/* Hover must be on the step/container, not the bead */
.ScrubberStep:hover .ScrubberBead {
  height: 0.75rem;
}
```

Apply the same principle to non-interactive composition: if a parent may already provide a border, define the border once at the correct container level so child styles don’t duplicate or partially render.