---
title: Graceful config validation
description: When configuration has conditional dependencies, make the system fail
  fast only for cases that break invariants (correctness/safety), but allow secure
  graceful degradation for “optional feature” toggles when prerequisites may be missing.
repository: maximhq/bifrost
label: Error Handling
language: Json
comments_count: 2
repository_stars: 6862
---

When configuration has conditional dependencies, make the system fail fast only for cases that break invariants (correctness/safety), but allow secure graceful degradation for “optional feature” toggles when prerequisites may be missing.

Apply this rule:
1) Enforce bidirectional relationships in schema
- If the meaning of one field depends on another (e.g., `auth_type`), use JSON Schema conditionals so invalid combinations are rejected rather than silently ignored.
- Prefer `allOf` with focused `if`/`then` blocks to avoid partial validation gaps.

Example (JSON Schema conditional enforcement):
```json
{
  "allOf": [
    {
      "if": {"properties": {"auth_type": {"const": "per_user_headers"}}, "required": ["auth_type"]},
      "then": {"required": ["per_user_header_keys"]}
    }
  ]
}
```

2) Don’t turn “safe no-ops” into hard failures
- For runtime-dependent options (e.g., requires object storage), if the runtime behavior is explicitly safe (e.g., “drop content, never leak”), keep schema validation non-fatal.
- Implement a one-time warning and fall back to the secure default instead of failing startup/validation.

Decision heuristic:
- If misconfiguration could lead to incorrect/unsafe behavior → enforce in schema (fail validation).
- If misconfiguration only disables functionality and the system guarantees secure fallback → allow it, warn, and degrade gracefully.