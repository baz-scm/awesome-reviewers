---
title: Use Canonical API Contracts
description: 'When integrating with platform services (SDKs or cloud APIs), treat
  the SDK/API surface as the source of truth: prefer built-in batch and “create-or-get”
  methods, consolidate overlapping client interfaces, and use structured configuration
  objects rather than ad-hoc parsing.'
repository: awslabs/agentcore-samples
label: API
language: Python
comments_count: 4
repository_stars: 3244
---

When integrating with platform services (SDKs or cloud APIs), treat the SDK/API surface as the source of truth: prefer built-in batch and “create-or-get” methods, consolidate overlapping client interfaces, and use structured configuration objects rather than ad-hoc parsing.

Apply this standard:
- Prefer platform SDK/API entrypoints over local “iterator/batch” reimplementations (remove unused custom loops when a batch API exists).
- Use SDK canonical idempotency helpers (e.g., `create_or_get_memory`) instead of duplicating try/except and “list then reuse” logic.
- Keep your public/CLI/API options unambiguous: don’t expose redundant low-level and higher-level “sdk/session” paths that do the same thing; explicitly separate concerns (e.g., control-plane create/delete vs data-plane session management).
- Parse inputs from structured config/request objects (e.g., `S3Location`-derived fields) rather than manual string splitting.
- Document client/API version requirements and deprecated parameters in code/docstrings so behavior doesn’t silently diverge across versions.

Example pattern (idempotent create-or-get):
```python
# Prefer SDK canonical idempotent helper
memory_id = memory_client.create_or_get_memory(name="my-session-memory")["id"]

# Prefer structured config instead of manual S3 parsing
# recording_config should already carry bucket/path fields
bucket = recording_config.s3_bucket
prefix = recording_config.s3_prefix
s3_uri = f"s3://{bucket}/{prefix}"
```

Result: fewer duplicated failure modes, stable client behavior across runs, and clearer request/response contracts for API consumers.