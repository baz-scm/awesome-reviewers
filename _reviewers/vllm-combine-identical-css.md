---
title: Combine identical CSS
description: When multiple CSS selectors share identical styling properties, combine
  them using comma separation rather than duplicating the same rules. This reduces
  code duplication, improves maintainability, and makes stylesheets more concise.
repository: vllm-project/vllm
label: Code Style
language: Css
comments_count: 2
repository_stars: 51730
---

When multiple CSS selectors share identical styling properties, combine them using comma separation rather than duplicating the same rules. This reduces code duplication, improves maintainability, and makes stylesheets more concise.

Example - Instead of this:
```css
.md-typeset .admonition.code,
.md-typeset details.code {
  border-color: #64dd17
}
.md-typeset .admonition.console,
.md-typeset details.console {
  border-color: #64dd17
}
```

Do this:
```css
.md-typeset .admonition.code,
.md-typeset details.code,
.md-typeset .admonition.console,
.md-typeset details.console {
  border-color: #64dd17;
}
```

This practice applies to all CSS rules with identical properties and values. By consolidating duplicate rules, you'll create more maintainable stylesheets that are easier to update and less prone to inconsistencies when making changes.