---
title: Async for slow work
description: When code performs potentially slow CPU/crypto work, avoid blocking the
  event loop. Prefer a Promise/callback-based asynchronous wrapper so the runtime
  can continue handling other work, and keep the function’s API surface consistent
  so it can replace a sync version without call-site changes. Also ensure your team’s
  documentation defines async accurately...
repository: 30-seconds/30-seconds-of-code
label: Concurrency
language: Markdown
comments_count: 2
repository_stars: 129334
---

When code performs potentially slow CPU/crypto work, avoid blocking the event loop. Prefer a Promise/callback-based asynchronous wrapper so the runtime can continue handling other work, and keep the function’s API surface consistent so it can replace a sync version without call-site changes. Also ensure your team’s documentation defines async accurately (e.g., “allow multiple events to trigger code without waiting for each other”).

Example (async wrapper that preserves the same call pattern):
```js
const crypto = require('crypto');

const hashNode = (val) =>
  new Promise((resolve) => {
    // Yield so other events can run before doing the expensive work
    setImmediate(() => {
      resolve(crypto.createHash('sha256').update(val).digest('hex'));
    });
  });
```

Apply this especially to server/request-heavy code paths where long hashing can delay other requests.