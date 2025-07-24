---
title: Maintain code consistency
description: 'Ensure consistent code organization, naming conventions, and structure
  throughout the codebase:


  1. Use identical parameter names for similar components (e.g., `queryGroup="language"`
  instead of custom names)'
repository: supabase/supabase
label: Code Style
language: Other
comments_count: 4
repository_stars: 86070
---

Ensure consistent code organization, naming conventions, and structure throughout the codebase:

1. Use identical parameter names for similar components (e.g., `queryGroup="language"` instead of custom names)
2. Place utility functions at appropriate scope levels - if a function has no component dependencies, define it outside the component
3. Apply proper semantic HTML structure (e.g., wrapping form elements in `<form>` tags)
4. Scope linting disables narrowly with `disable-next-line` rather than disabling for entire files

```jsx
// GOOD: Consistent parameter naming
<Tabs type="underlined" queryGroup="language">

// GOOD: Function properly scoped outside component
const generateNonce = async (): Promise<string[]> => {
  // implementation
}

function MyComponent() {
  // component code using generateNonce
}

// GOOD: Proper semantic structure
<form>
  <input type="email" />
  <input type="password" />
  <button type="submit">Submit</button>
</form>

// GOOD: Narrowly scoped linting disable
{/* supa-mdx-lint-disable-next-line Rule003Spelling */}
```

These consistent practices improve code readability, maintainability, and ensure predictable behavior across the application.