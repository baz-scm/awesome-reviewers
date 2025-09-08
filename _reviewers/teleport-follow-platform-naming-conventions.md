---
title: Follow platform naming conventions
description: Always use the correct naming conventions for the platform you're working
  with, particularly React and HTML standards. React has specific prop naming requirements
  that differ from HTML attributes, and using incorrect names can cause functionality
  to break or behave unexpectedly.
repository: gravitational/teleport
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 19109
---

Always use the correct naming conventions for the platform you're working with, particularly React and HTML standards. React has specific prop naming requirements that differ from HTML attributes, and using incorrect names can cause functionality to break or behave unexpectedly.

Key examples:
- Use `readOnly` instead of `readonly` for React props
- Follow React's camelCase convention for HTML attributes (e.g., `className`, `htmlFor`)
- Verify that props are valid for the target HTML elements (e.g., checkboxes and radio buttons don't support `readOnly`)

Example from the codebase:
```tsx
// ❌ Incorrect - invalid prop name
{props.readonly ? (
  <ReadOnlyCheckboxInternal />
) : (
  <CheckboxInternal />
)}

// ✅ Correct - follows React naming convention  
{props.readOnly ? (
  <ReadOnlyCheckboxInternal />
) : (
  <CheckboxInternal />
)}
```

When in doubt, consult the official React documentation or MDN for the correct prop names and supported attributes for specific HTML elements.