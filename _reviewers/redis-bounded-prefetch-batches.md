---
title: Bounded Prefetch Batches
description: 'When adding performance optimizations (prefetch/batching/fast paths),
  make them bounded, gated, and semantics-correct:


  - **Bound the work**: use fixed small batch sizes (e.g., 16) and stack-backed buffers
  with a safe default cap; avoid strategies where user-controlled sizes can force
  huge allocations (e.g., `vecReserve(count)` without a ceiling).'
repository: redis/redis
label: Performance Optimization
language: C
comments_count: 9
repository_stars: 74261
---

When adding performance optimizations (prefetch/batching/fast paths), make them bounded, gated, and semantics-correct:

- **Bound the work**: use fixed small batch sizes (e.g., 16) and stack-backed buffers with a safe default cap; avoid strategies where user-controlled sizes can force huge allocations (e.g., `vecReserve(count)` without a ceiling).
- **Gate the fast path**: only prefetch/batch when it’s likely to help (e.g., skip when cross-command prefetch already warmed the cache, or when the dict/slot has nothing to look up).
- **Preserve correctness**: fast paths must mirror the “real” iterator semantics (expired-field handling, `allow_access_expired`/skip behavior, and cluster/slot/dict lifetime across batches). If batch boundaries can change pointers (e.g., expire+free), re-fetch per batch.
- **Avoid redundant expensive work**: don’t repeat lookups/scans that the caller or batch already computed; prefer passing/reusing computed state instead of re-deriving it.

Example pattern (batch + gate + bounded stack, with a hard ceiling):

```c
#define BATCH_SZ 16
#define STACK_CAP 256

void do_fast_prefetch_and_reply(client *c, dict *d, int use_prefetch) {
    int numkeys = c->argc - 1;
    addReplyArrayLen(c, numkeys);

    /* Gate: only prefetch if there is something to warm. */
    if (!use_prefetch || d == NULL || dictSize(d) == 0) {
        for (int j = 1; j < c->argc; j++) {
            kvobj *o = lookupKeyRead(c->db, c->argv[j]);
            if (o == NULL || o->type != OBJ_STRING) addReplyNull(c);
            else addReplyBulk(c, o);
        }
        return;
    }

    /* Bounded batch work. */
    int j = 1;
    while (j < c->argc) {
        int end = j + BATCH_SZ;
        if (end > c->argc) end = c->argc;
        int n = end - j;

        /* Re-fetch any pointer that may become invalid across batch boundaries. */
        d = kvstoreGetDict(c->db->keys, /*slot*/0);
        if (d == NULL || dictSize(d) == 0) {
            for (int k = 0; k < n; k++) {
                lookupKeyRead(c->db, c->argv[j + k]);
                addReplyNull(c);
            }
            j = end;
            continue;
        }

        /* Prefetch within the bounded batch. */
        for (int k = 0; k < n; k++)
            redis_prefetch_read(&d->ht_table[0][0]); /* placeholder */

        for (int k = 0; k < n; k++) {
            kvobj *o = lookupKeyRead(c->db, c->argv[j + k]);
            if (o == NULL || o->type != OBJ_STRING) addReplyNull(c);
            else addReplyBulk(c, o);
        }
        j = end;
    }
}
```

Apply this checklist in code reviews for any performance PR: if the optimization can turn into unbounded allocation, double-prefetch, or semantic drift across expiry/cluster boundaries, it should be reworked to add bounding + gating + semantic parity.