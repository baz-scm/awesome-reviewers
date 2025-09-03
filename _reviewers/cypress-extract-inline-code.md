---
title: Extract inline code
description: Extract complex inline code elements into separate functions, components,
  or constants to improve readability and maintainability. This includes hardcoded
  strings, complex event handlers, and lengthy JSX expressions.
repository: cypress-io/cypress
label: Code Style
language: TSX
comments_count: 3
repository_stars: 48850
---

Extract complex inline code elements into separate functions, components, or constants to improve readability and maintainability. This includes hardcoded strings, complex event handlers, and lengthy JSX expressions.

Examples of what to extract:
- Hardcoded strings: Move to constants or props instead of inline literals
- Complex event handlers: Extract into separate functions rather than defining inline
- Complex JSX expressions: Pull into separate components when they contain significant logic or styling

```js
// Instead of inline handler:
onClick={(e) => {
  props.onClick(e, props.item)
  onClick(e, props.item)
}}

// Extract to function:
function handleClick(e) {
  props.onClick(e, props.item)
  if (props.item.onClick) {
    props.item.onClick(e, props.item)
  }
}
```

This practice makes code more testable, reusable, and easier to understand by giving meaningful names to code blocks and reducing visual complexity in the main component logic.