---
title: Safe URL/SVG Escaping
description: When building URL-like strings that will be embedded into SVG attributes
  (e.g., `marker-end="url(...)"`), do not rely on upstream HTML escaping. Apply context-specific
  escaping/encoding for the exact attribute syntax, ensuring correct escaping order
  (notably escape backslashes first) and covering all unsafe characters—not just parentheses.
repository: mermaid-js/mermaid
label: Security
language: Markdown
comments_count: 1
repository_stars: 87952
---

When building URL-like strings that will be embedded into SVG attributes (e.g., `marker-end="url(...)"`), do not rely on upstream HTML escaping. Apply context-specific escaping/encoding for the exact attribute syntax, ensuring correct escaping order (notably escape backslashes first) and covering all unsafe characters—not just parentheses.

Example pattern:

```js
function escapeForSvgUrlAttribute(input) {
  // Escape order matters: backslash must be escaped before other replacements.
  return input
    .replace(/\\/g, '\\\\') // backslash first
    .replace(/['"\s]/g, encodeURIComponent) // also handle quotes/whitespace
    .replace(/[()]/g, (m) => '\\' + m); // e.g., parentheses
}

const url = `http://localhost:9000/flowchart.html?hi=${escapeForSvgUrlAttribute(s)}`;
markerEnd = `url(${url}#id)`;
```

Also ensure the stricter escaping is applied in the sensitive code path(s) (e.g., only the branch where the absolute marker URL is constructed), since that’s where malformed/incorrect `url(...)` expressions can break rendering and undermine safety assumptions.