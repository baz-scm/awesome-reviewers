---
title: Assert meaningful outcomes
description: When writing tests, validate the *actual user-visible behavior and structured
  error data*, not just a substring or a indirectly implied result. Make failures
  unambiguous (no swallow-pass patterns) and keep tests easy to debug.
repository: colinhacks/zod
label: Testing
language: TypeScript
comments_count: 8
repository_stars: 42628
---

When writing tests, validate the *actual user-visible behavior and structured error data*, not just a substring or a indirectly implied result. Make failures unambiguous (no swallow-pass patterns) and keep tests easy to debug.

Apply this standard:
- Prefer full message assertions (especially for formatted/translated strings) and assert structured fields like `error.path` / `error.details` when those are part of the contract.
- Avoid patterns that can accidentally always pass (e.g., empty `try/catch` without assertions inside).
- For behavior with control-flow semantics (e.g., `fatal`), add tests that prove the flow stops/continues, not only that an error exists.
- Cover realistic inputs and edge cases; add additional cases when current regex/validation logic is suspected incomplete.
- Improve debugging and maintenance with table-driven tests (`test.each` / equivalent) instead of ad-hoc concatenation.
- Where type-level expectations matter, add type tests (e.g., with `tsd`) rather than relying solely on compile-time errors.

Example (meaningful runtime assertions):
```ts
const result = schema.safeParse(badInput);
expect(result.success).toBe(false);
if (!result.success) {
  expect(result.error.issues[0].message).toBe("full expected message");
  expect(result.error.issues[0].path).toEqual(['points']);
}
```
Example (prove `fatal` stops):
```ts
const schema = z
  .object({ test: z.literal(true) })
  .nullable()
  .refine(v => v !== null, { message: 'foo', fatal: true })
  .superRefine((v, ctx) => { if (v && (v as any).test) ctx.addIssue({ code: 'custom', message: 'bar' }); });

const out = schema.safeParse(null);
expect(out.success).toBe(false);
expect(out.error.issues.map(i => i.message)).toEqual(['foo']);
```
