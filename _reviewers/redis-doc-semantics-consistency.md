---
title: Doc Semantics Consistency
description: 'Ensure comments and public-facing documentation precisely match the
  actual behavior and contract.


  Apply this standard by checking:

  - **No doc/behavior drift**: If you add/adjust command options (e.g., STRICT/PERSIST)
  or state transitions (e.g., TTL handling), update all descriptions (PR text, command
  docs, inline comments) to reflect the implemented...'
repository: redis/redis
label: Documentation
language: C
comments_count: 8
repository_stars: 74261
---

Ensure comments and public-facing documentation precisely match the actual behavior and contract.

Apply this standard by checking:
- **No doc/behavior drift**: If you add/adjust command options (e.g., STRICT/PERSIST) or state transitions (e.g., TTL handling), update all descriptions (PR text, command docs, inline comments) to reflect the implemented semantics.
- **Define exact meaning of outputs/fields**: For INFO/metrics and API parameters, state what is included/excluded and what the field represents (e.g., “count is number of field names, not values”; “shared vs unshared bytes”).
- **Document semantic edge cases**: If duplicates are possible (e.g., subkey field names) or behavior depends on flags/invariants, explicitly document the expectation and any performance-vs-deduplication tradeoff.
- **Clarify unit/size semantics**: When a function returns a *requested* value rather than an *allocated* one, document that explicitly and ensure call sites don’t rely on the wrong notion.
- **Explain non-trivial logic**: For complex algorithms or rate-limiting behavior, include a short rationale/step summary in comments so maintainers can follow the intent.
- **Justify magic constants**: For bounds like a specific upper limit, add the reason (e.g., overflow/representable range) and keep the check consistent.

Example (magic constant rationale):
```c
if (period <= 0 || period >= 1000000000000LL) {
    /* 1e12 chosen so that when converting to microseconds we stay within int64 range */
    addReplyError(c, "period must be > 0 and < 1e12");
    return;
}
```

Rule of thumb: if someone can misinterpret the contract from the docs (TTL semantics, count semantics, shared-vs-unshared accounting, requested-vs-allocated), fix the documentation until the interpretation is unambiguous.