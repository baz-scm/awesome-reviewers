---
title: Container-first UI CSS
description: 'Apply CSS so layout/visual structure lives on the stable container,
  and interactive states target the stable hit area.


  - Borders/structural lines: define borders on the outer container that fully owns
  the visual edge. Avoid setting the same border on inner elements that can cause
  duplication when composed with a parent.'
repository: facebook/react#b3
label: Code Style
language: Css
comments_count: 2
repository_stars: 251883
---

Apply CSS so layout/visual structure lives on the stable container, and interactive states target the stable hit area.

- Borders/structural lines: define borders on the outer container that fully owns the visual edge. Avoid setting the same border on inner elements that can cause duplication when composed with a parent.
- Hover/focus correctness: attach `:hover`/listeners and the visual state changes to a non-animating hit target (e.g., the button/step). Don’t base `:hover` on the element that changes size (which can move the pointer off the hovered element and cause jitter/loops). Keep animated parts from “popping” outside the hit target using fixed sizing and `overflow: hidden` where appropriate.

Example pattern:
```css
/* Outer hit target owns layout + interaction */
.SuspenseScrubberStep {
  cursor: pointer;
  flex: 1;
  display: flex;
  align-items: center;
}

/* Animated inner element should not be the hover target */
.SuspenseScrubberBead {
  height: 0.5rem;
  overflow: hidden; /* or clip via parent container */
  transition: height 150ms ease;
}

/* State changes triggered by hovering the stable hit target */
.SuspenseScrubberStep:hover .SuspenseScrubberBead {
  height: 0.75rem;
}
```

Use the same principle for focus: keep focus outlines on the stable interactive container (e.g., `:focus-visible`), not on elements that move during interaction.