---
title: Await Connection Drains
description: When async work depends on a connection that may still be resolving,
  prevent startup race conditions by (1) deferring the work to an “early” queue instead
  of silently skipping, and (2) awaiting the connection setup promises before concluding/awaiting
  the deferred work.
repository: maximhq/bifrost
label: Concurrency
language: JavaScript
comments_count: 2
repository_stars: 6862
---

When async work depends on a connection that may still be resolving, prevent startup race conditions by (1) deferring the work to an “early” queue instead of silently skipping, and (2) awaiting the connection setup promises before concluding/awaiting the deferred work.

Apply this by standardizing the pattern:
- If the required DB/connection isn’t ready yet, enqueue the verification (do not SKIP).
- Once the connection resolves, drain the queue and push the resulting promises into your main pending list.
- In the final “done”/completion handler, await ALL connectionPromises first, then await Promise.allSettled(pendingVerifications).

Example pattern:
```js
const earlyCostingQueue = [];
const connectionPromises = [];
const pendingVerifications = [];

function verifyLaterOrQueue({ reqId, name }) {
  const expectCost = getHeader(/* request */ null, 'x-bf-expect-cost');
  if (expectCost && /^(1|true|yes)$/i.test(String(expectCost))) {
    if (!logsDbReady || !logsDb) {
      // Defer instead of silently skipping
      earlyCostingQueue.push({ reqId, name });
      return;
    }
    pendingVerifications.push(verifyCostingRequest(logsDb, reqId, name, results, silent));
  }
}

function drainCostingQueue(activeLogsDb) {
  while (earlyCostingQueue.length > 0) {
    const item = earlyCostingQueue.shift();
    pendingVerifications.push(verifyCostingRequest(activeLogsDb, item.reqId, item.name, results, silent));
  }
}

// Track connection resolution so drains happen before final wait
connectionPromises.push(connectLogsDb().then(activeLogsDb => {
  drainCostingQueue(activeLogsDb);
}));

// Finalization: await drains before awaiting pending work
Promise.allSettled(connectionPromises)
  .then(() => Promise.allSettled(pendingVerifications))
  .then(() => done());
```

Also ensure your core verification logic runs before any status-based early returns (e.g., before “2xx-skip”) so failure/cancelled cases aren’t accidentally bypassed.