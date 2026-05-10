---
title: Header Organization And Comments
description: 'Keep header edits readable and durable:


  1) Don’t write brittle comments

  - Avoid referencing exact line numbers or file offsets (they drift and become misleading).
  Prefer describing the behavior/why, not where it currently is.'
repository: redis/redis
label: Code Style
language: Other
comments_count: 4
repository_stars: 74261
---

Keep header edits readable and durable:

1) Don’t write brittle comments
- Avoid referencing exact line numbers or file offsets (they drift and become misleading). Prefer describing the behavior/why, not where it currently is.

2) Group declarations by concept in headers
- Place new structs/functions near the related types/metadata they operate on (e.g., keep kvstore-related metadata together; place “context” structs beside the owning feature’s metadata blocks).
- Don’t move unrelated APIs into headers just because they’re being touched—keep them in the header that matches their domain/ownership (e.g., robj/kvobj-related declarations in object.h; “server command/memory command”-style helpers remain in their original area).

3) Avoid unnecessary exposure
- If a new symbol is only used by one module, consider removing it from broader headers or narrowing its scope instead of exporting it.

Example (durable comment):
```c
// Bad: “Fix for crash at file.c:1234” (will rot)
// Good: Explain the invariant/ordering requirement that prevents stale pointers.
// e.g., “Ensure notification happens after all kvobj accesses to avoid stale pointers
// if the notification callback reallocates the kvobj.”
```

Example (grouping):
- Put `asmTrimCtx` right after the kvstore metadata structs it supports, and keep `kvstoreMetadata` adjacent to `kvstoreDictMetadata` rather than splitting them across the file.