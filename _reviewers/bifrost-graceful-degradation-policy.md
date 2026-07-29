---
title: Graceful Degradation Policy
description: 'For external dependencies that are *additive* (e.g., mirrors/archives)
  rather than required for correctness, prefer **fail-open** behavior: log errors
  and continue operating using the primary source of truth. Reserve **fail-fast**
  for dependencies that are *hard requirements* for correctness or API functionality.'
repository: maximhq/bifrost
label: Error Handling
language: Other
comments_count: 2
repository_stars: 6862
---

For external dependencies that are *additive* (e.g., mirrors/archives) rather than required for correctness, prefer **fail-open** behavior: log errors and continue operating using the primary source of truth. Reserve **fail-fast** for dependencies that are *hard requirements* for correctness or API functionality.

Practical rules:
- Classify each dependency/feature as either:
  - **Critical (correctness-gating):** if unavailable at startup or runtime, fail fast (or reject requests) to avoid silently incorrect behavior.
  - **Additive (mirror/archive/log sink):** if unavailable, continue core writes/operations; record the error for observability.
- Ensure the primary store remains the source of truth (e.g., DB-only audit logging still works).
- At startup and during batch flushes:
  - Catch connection/unreachability errors.
  - **Log + emit metrics**.
  - Do not block startup or request handling.
- Document the policy difference explicitly so teams don’t “standardize” into the wrong behavior.

Example (non-blocking additive sink):
```pseudo
onStartup():
  try:
    objectStoreClient = connect(config.objectStorage)
    archivalEnabled = true
  catch err:
    log.error("object storage unreachable; continuing database-only", err)
    archivalEnabled = false

writeAuditEvent(event):
  dbWrite(event) // must always succeed for correctness

flushBatch(batch):
  if not archivalEnabled: return
  try:
    objectStore.put(renderKey(batch), gzip(jsonl(batch)))
  catch err:
    log.error("archival upload failed; audit DB write already committed", err)
    // do not fail request handling
```