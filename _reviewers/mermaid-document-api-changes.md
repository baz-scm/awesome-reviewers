---
title: Document API Changes
description: 'When you change an exported/non-trivial API (or add new function parameters),
  update JSDoc so it is complete and directly helpful:


  - For every added/changed parameter: include a `{type}` and a short description
  of what the parameter controls.'
repository: mermaid-js/mermaid
label: Documentation
language: JavaScript
comments_count: 2
repository_stars: 87952
---

When you change an exported/non-trivial API (or add new function parameters), update JSDoc so it is complete and directly helpful:

- For every added/changed parameter: include a `{type}` and a short description of what the parameter controls.
- For deprecations: use `@deprecated` and point to the replacement using a link (e.g., `{@link NewSymbol}`), not just plain text.

Example (parameter documentation)
```js
/**
 * @param {any} node
 * @param {number} [width] - Max/target label width used for wrapping calculations.
 * @param {boolean} [addBackground=false] - Whether to apply the label background styling.
 * @returns {Promise<SVGForeignObjectElement>}
 */
async function addHtmlLabel(node, width, addBackground = false) {
  // ...
}
```

Example (deprecation documentation)
```js
/**
 * @deprecated Use {@link getBoundaries} instead
 */
export const getBoundarys = getBoundaries;
```