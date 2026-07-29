---
title: Concurrency-safe retries
description: 'When concurrency is involved, ensure two things: (1) your tests/operations
  can’t accidentally contend on shared resources, and (2) any concurrency-handling
  you add (e.g., retrying on 409) is only applied to errors that are truly reachable
  from the concurrent scenario you’re mitigating.'
repository: maximhq/bifrost
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 6862
---

When concurrency is involved, ensure two things: (1) your tests/operations can’t accidentally contend on shared resources, and (2) any concurrency-handling you add (e.g., retrying on 409) is only applied to errors that are truly reachable from the concurrent scenario you’re mitigating.

Apply this standard as follows:
- Use run/worker-unique identifiers for any created resources (keys, records, filenames) so parallel CI runs can’t collide and corrupt each other’s cleanup.
- Don’t add “catch-and-retry” for lock/in-flight errors unless the backend guarantees that error is produced by the concurrent path you’re exercising. If the error guard is unreachable for that path, retrying will only mask real failures.

Example (test isolation + no blind retry):
```ts
import { randomUUID } from "crypto";

// Run-scoped suffix prevents cross-run collisions on shared backends.
const runId = randomUUID().slice(0, 8);
const keyName = `Refresh-Key-${runId}`;

// Prefer waiting for the UI/request to settle rather than retrying on errors
// you can’t actually produce from this code path.
await page.click(refreshBtn);
await expect(refreshBtn).toBeEnabled({ timeout: 15000 });
```

If you’re considering retries for a specific error code, first verify (via server logic/guards) that the code is reachable under the scenario you’re trying to handle; otherwise avoid swallowing it and fix the scenario instead.