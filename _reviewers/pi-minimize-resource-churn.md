---
title: Minimize Resource Churn
description: 'Prefer designs that avoid unnecessary resource usage—especially filesystem
  churn and redundant persistence/reload.


  - For temporary artifacts, use the OS-managed temp directory (so cleanup is automatic)
  rather than creating long-lived app-specific temp folders.'
repository: earendil-works/pi
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 79783
---

Prefer designs that avoid unnecessary resource usage—especially filesystem churn and redundant persistence/reload.

- For temporary artifacts, use the OS-managed temp directory (so cleanup is automatic) rather than creating long-lived app-specific temp folders.
- For state updates, follow the existing established `setXXX` patterns: don’t introduce redundant `save()`/reload cycles when a simple in-memory update (or the same approach used elsewhere) suffices.

Example (OS temp dir for temporary work):
```ts
import { mkdtemp, rm } from "node:fs/promises";
import os from "node:os";
import { join } from "node:path";

// Use system temp root to avoid accumulating data under a home directory.
const tempRoot = await mkdtemp(join(os.tmpdir(), "agent-"));
try {
  // ... write/edit temp files ...
} finally {
  // Ensure cleanup even if OS doesn’t immediately collect.
  await rm(tempRoot, { recursive: true, force: true });
}
```

Example (settings update pattern):
- If other `setXXX` methods update `this.settings`/`globalSettings` directly without extra reload work, mirror that approach and avoid adding additional persistence/reload steps unless correctness requires it.