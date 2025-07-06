---
title: Safe property access patterns
description: Use appropriate null/undefined handling techniques based on the context
  to prevent runtime errors. Be mindful of the distinction between `null` and `undefined`
  in TypeScript, as they behave differently and affect type safety.
repository: grafana/grafana
label: Null Handling
language: TSX
comments_count: 4
repository_stars: 68825
---

Use appropriate null/undefined handling techniques based on the context to prevent runtime errors. Be mindful of the distinction between `null` and `undefined` in TypeScript, as they behave differently and affect type safety.

For accessing potentially undefined nested properties:
- Use optional chaining (`?.`) for succinct null-safe property access
- Consider lodash's `get()` for complex paths or when you need a default value
- Add proper type narrowing with conditional checks before accessing properties

When defining component props:
- Use `prop?: Type` for truly optional props (results in `undefined` when not provided)
- Use `prop: Type | null` when the absence of a value needs explicit representation
- Be consistent with your approach as mixing can lead to type issues

```typescript
// AVOID: Unnecessary null checks when types guarantee non-null
title={title?.toString()} // Not needed if title is always defined

// AVOID: Unsafe property access without null checking
// @ts-ignore
acc[name] = config.custom.cellOptions.type; // May cause runtime errors

// BETTER: Use optional chaining or conditional checks
if (config?.custom?.cellOptions?.type) {
  acc[name] = config.custom.cellOptions.type;
}

// BETTER: For complex paths, use lodash get with default values
const value = name ? get(formValues, name, '') : '';
```

Distinguish between unnecessary null checks (which add noise) and missing null checks (which cause bugs). Let TypeScript's type system guide your null-handling needs while maintaining runtime safety.