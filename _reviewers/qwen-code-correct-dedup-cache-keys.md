---
title: Correct Dedup Cache Keys
description: 'When implementing cursor-based dedup/caching for event dispatch, ensure
  the dedup “key space” matches the real uniqueness of what you’re trying to prevent:'
repository: QwenLM/qwen-code
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 26407
---

When implementing cursor-based dedup/caching for event dispatch, ensure the dedup “key space” matches the real uniqueness of what you’re trying to prevent:

- **Key on the right unit of change**: using a stable thread id alone can permanently suppress future events. Prefer composite keys (e.g., include event timestamp/version).
- **Record dedup after successful dispatch in every lane/path**: if one lane fetches content (comments/body/trigger) but doesn’t persist its dedup keys, another lane will re-fetch and re-dispatch the same items.
- **Apply both lower and upper bounds when re-discovering triggers**: after cursor eviction/trim, omitting the lower-bound (windowSince) can resurrect stale triggers.
- **Maintain cursor trims across all dedup buckets**: if you trim one list but not the others, dedup correctness degrades over time.
- **Be careful with caching headers**: don’t apply cacheable/read headers to transient error responses.

Practical template:
```ts
// 1) Dedup key must change when the triggering content changes.
const notifKey = `${notification.id}|${notification.updated_at}`; // not just notification.id

if (this.isDispatched(this.cursor.dispatchedNotifications, notifKey)) return;

// 2) Dispatch
await this.handleInbound(envelope);

// 3) Persist dedup keys for the exact items you dispatched
this.recordDispatched('dispatchedComments', dedupKey);
this.recordDispatched('dispatchedBodies', `${chatId}|${threadId}`);
this.recordDispatched('dispatchedEvents', triggerKey);

// 4) When re-discovering triggers, include both bounds
const event = events.findLast((candidate) => {
  const t = candidate.created_at;
  return t && t <= ctx.maxUpdatedAt && t > ctx.windowSince;
});
```

Acceptance checklist for reviews:
1) Every dispatch path has a corresponding, persisted dedup record (comments/bodies/events) on success.
2) Dedup keys include all dimensions needed to distinguish distinct “things to dispatch.”
3) Trigger search uses the same window bounds as the comment/body fetch logic.
4) Cursor trimming covers every dedup bucket you rely on.
5) HTTP read/caching headers are only applied on non-error response branches (or explicitly proven safe).