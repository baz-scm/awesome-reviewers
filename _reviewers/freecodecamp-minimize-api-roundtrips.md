---
title: Minimize API Roundtrips
description: When the client performs a state-changing action, design the API contract
  so it can be completed in as few requests as possible—prefer batch-capable endpoints
  and responses that include what the client needs to update UI/state without additional
  “refresh” calls. Also, for one-way boolean updates where the server can infer intent,
  avoid unnecessary request...
repository: freeCodeCamp/freeCodeCamp
label: API
language: TSX
comments_count: 3
repository_stars: 444449
---

When the client performs a state-changing action, design the API contract so it can be completed in as few requests as possible—prefer batch-capable endpoints and responses that include what the client needs to update UI/state without additional “refresh” calls. Also, for one-way boolean updates where the server can infer intent, avoid unnecessary request bodies.

Apply this as follows:
- Prefer server-side batching: if the client currently loops per item (and adds delays/rate-limit workarounds), provide an endpoint that accepts an array of IDs.
- Avoid client re-fetches after mutations: don’t call a broad “fetch user/account” just to learn the mutation result; return the updated/derived data from the mutation endpoint.
- Simplify one-way updates: if an endpoint always sets a field to a constant (e.g., `true`), don’t require a payload that just repeats that constant.

Example (batch endpoint shape):
```ts
// Instead of calling per block with rate-limit delays
// await deleteResetModule({ blockId: currentBlock }) in a loop

// Prefer one request with all IDs
await deleteResetModules({ blockIds: blockIds });
```

Example (mutation returns data to update client state):
```ts
const res = await resetModule({ moduleId });
// res should include the updated state the UI needs
setStateFromResponse(res);
// Don’t call a separate fetchUser() just to refresh UI.
```