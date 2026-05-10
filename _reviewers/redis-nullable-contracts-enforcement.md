---
title: Nullable Contracts Enforcement
description: 'Adopt explicit, consistent nullability contracts for pointer/optional-field
  parameters and honor them at every call site.


  Practical rules:

  - **Document/decide whether a parameter may be NULL**. If it can’t, keep the check
  out; if it can, guard and define behavior.'
repository: redis/redis
label: Null Handling
language: C
comments_count: 9
repository_stars: 74261
---

Adopt explicit, consistent nullability contracts for pointer/optional-field parameters and honor them at every call site.

Practical rules:
- **Document/decide whether a parameter may be NULL**. If it can’t, keep the check out; if it can, guard and define behavior.
- **Align new helpers with existing conventions** (e.g., `get*From*Object` patterns) so developers don’t guess whether NULL is legal.
- **Guard before dereference** when an optional field can be absent (e.g., `if (obj->field) { use }`).
- **Avoid UB from “meaningless” fields**: don’t read dict values when the dict is configured for `no_value`; pass/handle the correct canonical value (`NULL` for absent value).
- **Prefer correctness via interface contracts over defensive checks inside low-level helpers** (unless the team has a specific safety requirement). If a helper would UB with bad inputs (e.g., `memcpy(dst,NULL,n>0)`), enforce the precondition at call sites.
- **After invalidation/nullification, treat pointers as unusable** (prevent accidental use-after-invalidate by structuring code flow so dereferences are impossible).

Example pattern:
```c
/* Optional pointer is truly nullable; guard before use */
if (nack->consumer) {
    addReplyBulkCBuffer(c, nack->consumer->name,
                        sdslen(nack->consumer->name));
} else {
    addReplyBulkCBuffer(c, "", 0);
}

/* Dict configured with no_value: never read dictGetVal() */
if (dictAdd(dst, key, NULL) == DICT_OK) {
    /* ... */
}
```

This standard prevents ambiguous NULL expectations, avoids undefined behavior, and keeps null-safety practical instead of scattered defensive code.