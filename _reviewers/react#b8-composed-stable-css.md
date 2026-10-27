---
title: Composed, Stable CSS
description: 'Write CSS so visuals and interactions have clear ownership and don’t
  cause layout/hover jitter.


  - **Own visuals at the correct container level.** Put borders (or other framing)
  on the outer container that should control the entire rendered area, so borders
  don’t span only part of the content and don’t get duplicated when parents also apply
  borders.'
repository: facebook/react#b8
label: Code Style
language: Css
comments_count: 2
repository_stars: 251889
---

Write CSS so visuals and interactions have clear ownership and don’t cause layout/hover jitter.

- **Own visuals at the correct container level.** Put borders (or other framing) on the outer container that should control the entire rendered area, so borders don’t span only part of the content and don’t get duplicated when parents also apply borders.

  ```css
  /* Prefer container ownership over partial element ownership */
  .label {
    padding: 0.25rem;
    color: var(--color-dimmer);
    font-style: italic;
    /* border moved to the container that spans the full layout */
  }
  .labelContainer {
    border-left: 1px solid var(--color-border);
  }
  ```

- **Attach `:hover`/focus selectors to the stable hit target, not the animating child.** If the hovered element’s animation changes its size/position, the pointer can leave the element and retrigger repeatedly. Instead, apply hover styles based on the outer “step” (the element that remains consistently sized).

  ```css
  .SuspenseScrubberStep {
    cursor: pointer;
    flex: 1;
    height: 100%;
    /* hit target is stable */
  }

  .SuspenseScrubberStep:hover .SuspenseScrubberBead {
    height: 0.75rem; /* animate bead, but hover comes from the step */
  }
  ```

- **Prevent hover-induced layout shifts.** Use **fixed height/line-height** (or fixed box sizing) and consider `overflow: hidden` so animated content doesn’t “pop” outside the hit target.

Applying these rules improves both maintainability (clear style ownership) and UX stability (no hover jitter).