---
title: avoid unclear abbreviations
description: 'Use clear, descriptive names instead of abbreviated variable names that
  reduce code readability. Abbreviations like `mult` should be replaced with more
  conventional or descriptive alternatives. Additionally, maintain consistent naming
  conventions: use `snake_case` for internal code and `camelCase` for user-facing
  APIs.'
repository: sveltejs/svelte
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 83580
---

Use clear, descriptive names instead of abbreviated variable names that reduce code readability. Abbreviations like `mult` should be replaced with more conventional or descriptive alternatives. Additionally, maintain consistent naming conventions: use `snake_case` for internal code and `camelCase` for user-facing APIs.

```js
// ❌ Avoid unclear abbreviations
export function multiplier(initial, mult) {
  return initial * mult;
}

// ✅ Use clear, conventional names
export function multiplier(initial, k) {
  return initial * k;
}

// ❌ Inconsistent naming between internal and external
component.$destroy(run_outro); // user-facing API using snake_case

// ✅ Consistent naming patterns
component.$destroy(runOutro); // user-facing API using camelCase
```

This approach improves code maintainability by making variable purposes immediately clear to other developers and ensures consistent patterns across different parts of the codebase.