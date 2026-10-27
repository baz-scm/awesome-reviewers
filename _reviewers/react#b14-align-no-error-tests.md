---
title: Align No-Error Tests
description: When testing or encoding error-handling behavior, ensure (1) the fixture
  or scenario name clearly matches the intended error policy, and (2) the code path
  is runnable so any thrown exception reflects the expected scenario—not an accidental
  runtime issue.
repository: facebook/react#b14
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 251893
---

When testing or encoding error-handling behavior, ensure (1) the fixture or scenario name clearly matches the intended error policy, and (2) the code path is runnable so any thrown exception reflects the expected scenario—not an accidental runtime issue.

Apply this by:
- For “no-error” scenarios, document the rationale for suppressing throws (e.g., when you can’t know whether a global call will trigger state updates) and keep the fixture naming consistent with that contract.
- For runtime verification, define any symbols used by the generated code as real runtime values (avoid type-only declarations that can produce unrelated exceptions).

Example (type-only vs runtime function):
```ts
// ❌ Can fail at runtime: used as a value but declared only as a type
declare function id<T>(x: T): T;

// ✅ Define as a runtime function so error-handling tests are meaningful
function id<T>(x: T): T {
  return x;
}
```

Result: your tests accurately validate the intended failure/suppression behavior and don’t introduce misleading exceptions that obscure the true error-handling contract.