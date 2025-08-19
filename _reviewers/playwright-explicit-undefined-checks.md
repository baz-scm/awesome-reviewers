---
title: explicit undefined checks
description: Always use explicit checks for undefined values and return appropriate
  nullable types instead of relying on implicit conversions or unsafe type assertions.
  Use modern JavaScript equality checks and proper TypeScript utility types for null
  safety.
repository: microsoft/playwright
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 76113
---

Always use explicit checks for undefined values and return appropriate nullable types instead of relying on implicit conversions or unsafe type assertions. Use modern JavaScript equality checks and proper TypeScript utility types for null safety.

When a function might not have a value to return, use `undefined` as the return type and check explicitly:

```typescript
// Good: Explicit undefined check and nullable return type
export function formatProtocolParam(params: Record<string, string> | undefined, alternatives: string): string | undefined {
  if (!params)
    return undefined;
  
  if (params[name] !== undefined)
    return params[name];
}

// Good: Use modern equality check
if (a.description === undefined) {
  // handle undefined case
}

// Good: Use proper TypeScript utility types
type HtmlReportOpenOption = NonNullable<Options['open']>;

// Avoid: Using 'any' when 'unknown' provides better type safety
async setFileChooserInterceptedBy(enabled: boolean, by: unknown): Promise<void> {
```

This approach prevents null reference errors, makes code intentions explicit, and leverages TypeScript's type system for compile-time safety rather than relying on runtime type coercion.