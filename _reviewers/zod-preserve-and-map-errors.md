---
title: Preserve and Map Errors
description: 'Standardize error handling so failures remain diagnosable and user-facing
  messages are complete.


  Apply these rules:

  1) Preserve diagnostic context when propagating/rethrowing'
repository: colinhacks/zod
label: Error Handling
language: TypeScript
comments_count: 8
repository_stars: 42628
---

Standardize error handling so failures remain diagnosable and user-facing messages are complete.

Apply these rules:
1) Preserve diagnostic context when propagating/rethrowing
- If you rebuild or re-aggregate errors, do not unintentionally lose stack trace/throw location. Centralize error creation/throwing so the actual `throw` happens in a predictable place, and avoid patterns that always create a fresh error object without considering stack semantics.

2) Ensure every issue code is explicitly mapped
- When adding a new `ZodIssueCode` (or changing which codes are emitted), update `defaultErrorMap` and/or locale maps so users don’t see generic fallback messages.

3) Extract/format messages safely (no unsafe casts)
- Don’t assume `catch (error)` is an `Error`. Prefer `instanceof Error` or a shared helper that guarantees a string.

4) Don’t unintentionally suppress other validations
- If you use early returns in validation logic, verify you’re not preventing other expected errors from being added for the same input.

Example: safe message extraction
```ts
try {
  return JSON.parse(val);
} catch (e: unknown) {
  const message = e instanceof Error ? e.message : String(e);
  ctx.addIssue({
    code: ZodIssueCode.invalid_string,
    validation: "json",
    message,
  });
}
```

Example: stack-preserving handler shape
```ts
const zodErrorHandler = (messageOrObject: string | unknown) => {
  if (typeof messageOrObject === "string") {
    throw ZodError.fromString(messageOrObject);
  }
  throw messageOrObject; // keep original throw semantics where possible
};
```

Checklist for PRs in this area
- [ ] New/changed `ZodIssueCode` has explicit message mapping (default + locales if needed).
- [ ] Validation control flow (early returns) can’t hide required additional issues.
- [ ] No `error as Error` without `instanceof` or a safe conversion helper.
- [ ] Error propagation/rewrap logic reviewed for stack/throw-location implications.