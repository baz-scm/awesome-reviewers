---
title: Semantic naming consistency
description: Choose semantically clear and consistent names across related elements
  in your codebase. Names should convey their purpose without requiring additional
  context or explanation, and related elements should follow consistent naming patterns.
repository: ant-design/ant-design
label: Naming Conventions
language: Markdown
comments_count: 5
repository_stars: 95882
---

Choose semantically clear and consistent names across related elements in your codebase. Names should convey their purpose without requiring additional context or explanation, and related elements should follow consistent naming patterns.

Key principles:
- Use descriptive names that clearly indicate functionality (e.g., `folder` vs `directory` where `folder` aligns with native behavior)
- Maintain consistency between related elements like filenames and display names (e.g., if changing "Icon Position" to "Icon Placement", also update the corresponding filename from `icon-position.tsx` to `icon-placement.tsx`)
- Avoid ambiguous or auto-generated identifiers (e.g., prefer `#inputsearch` over `#inputsearch-1`)
- Follow consistent ordering patterns for API documentation (alphabetical for properties, then methods)

Example:
```jsx
// Good: Semantic and consistent naming
<code src="./demo/icon-placement.tsx">Icon Placement</code>

// Bad: Inconsistent between filename and display
<code src="./demo/icon-position.tsx">Icon Placement</code>
```

This ensures code is self-documenting and maintainable, reducing confusion for developers who encounter the code without prior context.