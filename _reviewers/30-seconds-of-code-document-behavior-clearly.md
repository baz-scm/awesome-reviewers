---
title: Document behavior clearly
description: For every snippet/glossary entry, the documentation must make the implementation’s
  behavior and constraints immediately clear—especially anything that can surprise
  users.
repository: 30-seconds/30-seconds-of-code
label: Documentation
language: Markdown
comments_count: 10
repository_stars: 129334
---

For every snippet/glossary entry, the documentation must make the implementation’s behavior and constraints immediately clear—especially anything that can surprise users.

Apply this checklist:
- Explain *how* it works (briefly, but concretely), not just the goal.
- Call out side effects and non-obvious behavior (e.g., whether it mutates inputs).
- Document required runtime/context constraints (Node vs browser, user-gesture requirements, feature availability).
- Include correctness aids: value ranges, links/references, and at least one clarifying example.
- Keep examples formatted consistently and copy/paste friendly (separate code blocks where appropriate).
- Avoid oversimplified/incorrect definitions in glossary terms.

Example pattern:
```js
// Converts HSV to RGB.
// HSV ranges: H in [0,360], S in [0,1], V in [0,1] (see linked reference).
// Returns: [r,g,b] as numbers.
// Notes: Works in any JS runtime.
function hsvToRgb(h, s, v) {
  // implementation...
}
```