---
title: Stable, Composable CSS
description: 'When writing CSS, prefer patterns that (a) compose cleanly across parent/child
  components and (b) keep interaction states stable.


  **1) Structural styles should live on the container**'
repository: facebook/react#b2
label: Code Style
language: Css
comments_count: 2
repository_stars: 251882
---

When writing CSS, prefer patterns that (a) compose cleanly across parent/child components and (b) keep interaction states stable.

**1) Structural styles should live on the container**
- Apply shared structural styling (e.g., borders) to the appropriate outer container so it spans the intended area.
- Avoid duplicating structural rendering when parents may already provide it.

**2) Put hover/focus on the hit target (not the animating piece)**
- If an element’s hover changes its own size/position, ensure the hover selector is on a stable outer element whose geometry won’t cause the hover to disappear/re-trigger (prevents “hover jitter” loops).
- Keep animated content within predictable dimensions; use fixed heights/line-height and clipping (e.g., `overflow: hidden`) so the hit target remains the outer box.

Example pattern:
```css
.Scrubber {
  position: relative;
  width: 100%;
  height: 1.5rem;
  border-radius: 0.75rem;
  padding: 0.25rem;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  overflow: hidden; /* keeps animation from popping outside hit target */
}

.ScrubberStep {
  flex: 1;
  height: 100%;
  padding-right: 1px; /* clickable pixels */
  cursor: pointer;
  display: flex;
  align-items: center;
}

/* Hover is on the stable step, not the animating bead */
.ScrubberStep:hover .Bead {
  height: 0.75rem;
}

.Bead {
  flex: 1;
  height: 0.5rem;
  transition: height 0.3s ease-in-out;
}
```

Applying these rules improves readability (clear ownership of styles), prevents duplicated visual chrome, and eliminates hover feedback loops caused by animating the hovered element itself.