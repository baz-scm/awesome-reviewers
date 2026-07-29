---
title: Failure-Safe State Handling
description: 'When error handling affects control-flow invariants (dedupe keys, stale-session
  guards, correctness checks), make failures safe and reversible:


  - Cleanup on every failure path: If you “remember”/lock/dedupe before completing
  the operation, ensure that early returns and catch blocks restore the pre-operation
  state (e.g., remove the remembered key).'
repository: nousresearch/hermes-agent
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 221948
---

When error handling affects control-flow invariants (dedupe keys, stale-session guards, correctness checks), make failures safe and reversible:

- Cleanup on every failure path: If you “remember”/lock/dedupe before completing the operation, ensure that early returns and catch blocks restore the pre-operation state (e.g., remove the remembered key).
- Don’t bypass correctness in catch: If a guard depends on remote/local state fetch, handle fetch errors explicitly. Don’t fall back to “proceed anyway” in a way that permits stale/out-of-date actions.
- Test recovery behavior: Add a retry regression test covering the failure scenario so the second attempt behaves correctly.

Example pattern (dedupe cleanup):
```ts
const dedupeKey = imageBlobDedupeKey(blob, data)
if (rememberRecentImageBlobPaste(refs, dedupeKey)) return
try {
  const ok = await saveImageBuffer(...)
  if (!ok) throw new Error('save failed')
} catch (e) {
  // restore invariant so immediate retry can attach
  forgetRecentImageBlobPaste(refs, dedupeKey)
  throw e
}
```
Example pattern (guard integrity):
```ts
try {
  const remote = await getSessionMessages(guardStoredId /* required routing */)
  // decide based on remote
} catch (e) {
  // safe default: block + refresh rather than submit with stale context
  await refreshSessionContext()
  return
}
```