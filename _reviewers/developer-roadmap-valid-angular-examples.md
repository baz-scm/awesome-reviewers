---
title: Valid Angular Examples
description: When adding Angular examples (docs, snippets, templates), ensure they
  are both *syntactically/semantically valid* and shown in the *correct template context*.
repository: kamranahmedse/developer-roadmap
label: Angular
language: Markdown
comments_count: 6
repository_stars: 354523
---

When adding Angular examples (docs, snippets, templates), ensure they are both *syntactically/semantically valid* and shown in the *correct template context*.

Key rules:
- **Signals in conditionals:** If a condition depends on a signal, **call** the signal (e.g., `count()`), rather than using the signal object directly.
- **Template blocks:** Show `@if` usage in an Angular **template/HTML** context (not in TS/logic examples), using valid template syntax.
- **Avoid misleading docs:** Don’t include examples that are known to always be truthy or otherwise incorrect; keep explanatory text and formatting clear.

Example (template context):
```html
<div class="user-container">
  @if (count() === 1) {
    <b>Count is 1</b>
  } @else {
    <b>Count is not 1</b>
  }
</div>
```

(And ensure `count` is a signal defined in the component, e.g., `const count = signal(0);`.)