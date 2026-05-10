---
title: Centralized input guards
description: Require a shared, spec-aligned “guard” step for any untrusted input used
  in security-sensitive contexts (SQL construction, dynamic table names, outbound
  URL fetch). Fail closed (raise a safe exception) before interpolation/requests,
  and reuse a single utility to avoid security-policy drift.
repository: infiniflow/ragflow
label: Security
language: Python
comments_count: 6
repository_stars: 80174
---

Require a shared, spec-aligned “guard” step for any untrusted input used in security-sensitive contexts (SQL construction, dynamic table names, outbound URL fetch). Fail closed (raise a safe exception) before interpolation/requests, and reuse a single utility to avoid security-policy drift.

Practical rules:
- SQL / identifier interpolation: validate identifiers (e.g., UUIDs) *before* using them in f-strings or dynamic table names; parameterize whenever possible.
- Reuse instead of duplicating: if an existing validation helper exists, ensure it matches the required constraints (e.g., don’t silently narrow “UUID version” rules) and raises the exception type your call site expects.
- Outbound fetch (SSRF): centralize URL safety checks in a shared utility; avoid per-endpoint ad-hoc rules.
- Logging hygiene: don’t log full user-supplied URLs (may contain credentials/tokens). Log minimal metadata (scheme/host or a redacted form).

Example pattern (UUID guard):
```python
import uuid
import logging
logger = logging.getLogger(__name__)

def assert_valid_uuid(value: str, *, label: str) -> str:
    try:
        # Validate; optionally canonicalize to the storage format your SQL expects
        return uuid.UUID(str(value)).hex  # e.g., 32-char form
    except (ValueError, TypeError):
        logger.warning("Rejected invalid %s (len=%d)", label, len(str(value)))
        raise ValueError(f"Invalid {label} format")

# Use only after guard
kb_hex = assert_valid_uuid(kb_ids[0], label="kb_id")
table_name = f"ragflow_{tenant_id}_{kb_hex}"
```

Example pattern (SSRF logging hygiene):
```python
# Instead of logging full URL:
logger.warning("SSRF guard blocked URL (scheme=%r host=%r)", scheme, parsed.hostname)
```