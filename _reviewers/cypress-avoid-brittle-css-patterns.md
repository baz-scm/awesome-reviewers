---
title: Avoid brittle CSS patterns
description: Write CSS that prioritizes maintainability and reduces the likelihood
  of conflicts or brittleness. This includes using semantic class names instead of
  raw HTML element selectors, and avoiding explicit z-index values when possible.
repository: cypress-io/cypress
label: Code Style
language: Css
comments_count: 2
repository_stars: 48850
---

Write CSS that prioritizes maintainability and reduces the likelihood of conflicts or brittleness. This includes using semantic class names instead of raw HTML element selectors, and avoiding explicit z-index values when possible.

Raw HTML selectors like `span:last-child button` and `span` are more brittle and harder to understand than semantic class names. Similarly, explicit z-index values like `z-index: 99999` can lead to stacking conflicts where developers "find themselves fighting with their own code on who's on top."

Instead, prefer:
- Semantic class names that clearly describe the component's purpose
- Natural document order and portal-based stacking for z-index management
- CSS patterns that are self-documenting and less likely to break when the HTML structure changes

Example of brittle pattern:
```css
span:last-child button,
.play {
  padding: 1px 10px;
}

.ui-blocker {
  z-index: 99999; /* Explicit z-index can cause conflicts */
}
```

Better approach:
```css
.header-action-button,
.play-button {
  padding: 1px 10px;
}

.ui-blocker {
  /* Rely on natural stacking order instead of explicit z-index */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
```