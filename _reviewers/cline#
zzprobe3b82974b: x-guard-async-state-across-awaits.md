---
title: Guard async state across awaits
description: Many bugs in this codebase came from code that resumes after an `await`
  and assumes nothing else touched the shared resource (a file, a session, a message
  list, a cache slot) in the meantime. Two complementary techniques fix this class
  of bug, and one of them should be applied whenever an async function reads, mutates,
  and later writes back shared mutable...
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Concurrency
language: TypeScript
comments_count: 14
repository_stars: 71067
---

Many bugs in this codebase came from code that resumes after an `await` and assumes nothing else touched the shared resource (a file, a session, a message list, a cache slot) in the meantime. Two complementary techniques fix this class of bug, and one of them should be applied whenever an async function reads, mutates, and later writes back shared mutable state:

1. **Serialize conflicting operations on the same key.** When two callers can race to read-modify-write the same resource (two patches to the same file, two status writes for the same session, two checkpoint commits updating "the last checkpoint message"), don't let them run concurrently — queue them behind a per-key lock/promise so the second waits for the first to finish before it reads. Example, keyed per-file queue:
```ts
const pendingEdits = new Map<string, Promise<void>>();

async function withFileLock<T>(path: string, fn: () => Promise<T>): Promise<T> {
  const prior = pendingEdits.get(path) ?? Promise.resolve();
  let release!: () => void;
  const next = new Promise<void>((resolve) => (release = resolve));
  pendingEdits.set(path, prior.then(() => next));
  await prior;
  try {
    return await fn();
  } finally {
    release();
    if (pendingEdits.get(path) === next) pendingEdits.delete(path);
  }
}
```
Capture the target *before* starting the async work (e.g. the exact message index/ts for a checkpoint commit) rather than re-searching for "the latest" item once the awaited work resolves — a concurrent operation may have appended a newer item in between.

2. **Stamp a generation/version token before the first await, and verify it after every subsequent await before applying a side effect (state mutation, dispatch, notification, resource teardown).** If the token no longer matches, the operation has been superseded (by a retry, a reload, an abort, a scope change, a reconnect) and must bail out without mutating shared state:
```ts
const generation = ++this.generation;
await doAsyncWork();
if (generation !== this.generation || this.disposed) return; // superseded; do nothing
this.apply(result);
```
Re-check immediately before every side effect that follows an await, not just once at the top of the function — a displacement can happen in any gap. Where a resource must stay alive for an in-flight operation (e.g. a connection pinned by a status check and a reopen running concurrently), use an explicit reference count/pin rather than relying on timing. Where an operation can be cancelled, make the abort synchronously mark state as cancelled *before* the first await so a concurrent waiter never mistakes it for live work.

Apply this discipline anywhere an async handler, hook, or RPC response can land after the state it was issued against has changed shape.