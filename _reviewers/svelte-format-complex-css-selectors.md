---
title: Format complex CSS selectors
description: When working with complex CSS selectors that include multiple nested
  pseudo-selectors like `:is()`, `:where()`, `:not()`, and `:has()`, maintain consistent
  formatting and consider breaking long selector chains for better readability. This
  is particularly important in Svelte components where selectors may need `:global()`
  wrappers.
repository: sveltejs/svelte
label: Code Style
language: Other
comments_count: 2
repository_stars: 83580
---

When working with complex CSS selectors that include multiple nested pseudo-selectors like `:is()`, `:where()`, `:not()`, and `:has()`, maintain consistent formatting and consider breaking long selector chains for better readability. This is particularly important in Svelte components where selectors may need `:global()` wrappers.

For complex nested selectors, consider adding multiple selector options within pseudo-selectors to improve maintainability:

```css
/* Good: Multiple selectors within :is() for flexibility */
div :is(:global(.class:is(span:is(:hover)), .x)){}

/* Instead of: Single complex nested chain */
div :is(:global(.class:is(span:is(:hover)))){}
```

This approach makes selectors more maintainable and allows for easier extension when additional selector variants are needed.