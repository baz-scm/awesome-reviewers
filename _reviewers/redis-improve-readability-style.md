---
title: Improve Readability Style
description: 'Adopt a “review-first” style for complex C code: keep control flow and
  conditions small, make side effects explicit, and avoid duplication.


  Key rules:'
repository: redis/redis
label: Code Style
language: C
comments_count: 8
repository_stars: 74261
---

Adopt a “review-first” style for complex C code: keep control flow and conditions small, make side effects explicit, and avoid duplication.

Key rules:
1) Split overly long conditionals
- Avoid putting multiple parsing/validation calls into a single large `if`.
- Prefer sequential guarded `if` blocks.

2) Use guard clauses and shared cleanup
- Reduce indentation by returning early on validation failures.
- When there are multiple paths (e.g., fast-path vs fallback), share cleanup via a single label or helper, so the structure stays flat.

3) Prefer explicit branching for special modes
- Don’t hide unusual behavior inside another branch (e.g., special aggregate handling mixed into SUM). Use `else if` with a clear name/comment.

4) Extract duplicated “finalization”/side-effect logic
- If multiple commands repeat the same update/notification/keyspace-finalization logic, move it to a helper to keep behavior consistent (and reduce the chance of diverging implementations).

5) Enforce consistent formatting
- Always use braces for multi-line `if/for/while` bodies.
- For multi-line conditions, wrap the controlled block with `{}` for scan-ability.

6) Use named constants instead of magic numbers
- Prefer existing shared constants (e.g., buffer sizing macros) over local ad-hoc values.

Example (splitting long validation):
```c
// Before (hard to read)
if (parseA()!=C_OK || parseB()!=C_OK || parseC()!=C_OK) return;

// After (reviewable)
if (parseA() != C_OK) return;
if (parseB() != C_OK) return;
if (parseC() != C_OK) return;
```

Example (shared cleanup to reduce indentation):
```c
if (fast_path_ok) {
    goto done;
}
// fallback path

done:
cleanup_common();
return;
```

Applying these consistently makes diffs easier to scan, reduces reviewer cognitive load, and prevents subtle behavioral drift across similar command implementations.