---
title: Fail/Clamp Error Contracts
description: 'When implementing commands with numeric failure modes (overflow, out-of-range,
  NaN/Inf) or multi-option parsing, define an explicit error contract and enforce
  it end-to-end:'
repository: redis/redis
label: Error Handling
language: C
comments_count: 8
repository_stars: 74261
---

When implementing commands with numeric failure modes (overflow, out-of-range, NaN/Inf) or multi-option parsing, define an explicit error contract and enforce it end-to-end:

1) Establish FAIL vs CLAMP semantics
- Default to FAIL: reject the operation (return an error) and do not modify the key.
- CLAMP (or equivalent): only under an explicit mode, saturate/cap to allowed bounds and proceed.
- Apply the same policy consistently to both implicit failures (type limits) and explicit failures (LBOUND/UBOUND).

2) Validate inputs and option combinations early
- Parse strictly and reject contradictory/incomplete options (e.g., STRICT/ONBOUND requires bounds).
- Prevent duplicate/repeated flags (e.g., BYINT specified twice).
- Resolve parsing ambiguity (e.g., if the stored value is float, don’t assume integer conversion can’t fail—fallback safely based on detected type/parse result).

3) Propagate errors immediately
- Treat conversion/parsing failures and corrupted data as hard failures (early return).
- For environment-dependent operations, prefer graceful fallback paths when syscalls fail.

4) Respect fatal subsystem state
- Don’t call “cleanup” helpers in states where the subsystem documented it must not be called after a fatal error (e.g., SSL fatal error states).

Example (numeric failure contract sketch):
```c
bool clamp_mode = (flags & OBJ_ONBOUND_CLAMP);

// Validate/parse first; no state mutation before checks.
if (parse_value_or_reply(c, &value) != C_OK) return;
if (parse_bounds_or_reply(c, &lb, &ub) != C_OK) return;

value2 = value + incr;
if (isnan(value2) || isinf(value2)) {
    addReplyError(c, "increment would produce NaN/Infinity");
    return; // FAIL always
}

if (value2 < lb || value2 > ub) {
    if (!clamp_mode) {
        addReplyError(c, "value is out of bounds");
        return; // do not modify key
    }
    value2 = (value2 < lb) ? lb : ub; // CLAMP
}

// Only now: perform the key update + reply.
set_key_value(c, value2);
```

Adopting this standard prevents inconsistent edge-case behavior, avoids partial updates on failure, and makes error handling predictable for both client-facing semantics and internal defensive safety.