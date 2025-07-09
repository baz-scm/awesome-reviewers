---
title: Precise documentation language
description: Use specific and clear language in all documentation to improve user
  understanding and avoid ambiguity. Favor precise terminology over vague descriptors,
  while balancing specificity with maintainability concerns.
repository: vitejs/vite
label: Documentation
language: Other
comments_count: 2
repository_stars: 74031
---

Use specific and clear language in all documentation to improve user understanding and avoid ambiguity. Favor precise terminology over vague descriptors, while balancing specificity with maintainability concerns.

Examples:
- Instead of referring to "the old version," specify the exact version number: "Vite 5 (old version)"
- Use semantically appropriate HTML elements in documentation (e.g., `<strong>` instead of `<b>`)
- When describing scope or applicability (like in license files or feature documentation), ensure language precisely defines the boundaries

```html
<!-- Instead of this -->
<p>
  This documentation describes <b>the old</b> Vite version. For the latest
  version, see <a href="https://vite.dev/">the latest document</a>.
</p>

<!-- Use this -->
<p>
  This documentation covers Vite 5 <strong>(old version)</strong>. For the latest
  version, see <a href="https://vite.dev">https://vite.dev</a>.
</p>
```

Consider the maintenance implications when determining how specific to be. Sometimes very precise details (like future version numbers) might create maintenance burden that outweighs the benefit of specificity.