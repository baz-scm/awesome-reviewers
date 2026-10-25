---
title: Preserve API Contracts
description: 'Ensure API contracts are explicit, semantically consistent, and forwarded
  end-to-end across layers.


  Practical rules:

  1) Don’t change semantics without changing the contract: if a request header field’s
  *meaning* changes, either keep the original meaning or rename the header (or add
  a new header) so the backend contract remains unambiguous.'
repository: ClInE/cLiNe
label: API
language: TypeScript
comments_count: 5
repository_stars: 70838
---

Ensure API contracts are explicit, semantically consistent, and forwarded end-to-end across layers.

Practical rules:
1) Don’t change semantics without changing the contract: if a request header field’s *meaning* changes, either keep the original meaning or rename the header (or add a new header) so the backend contract remains unambiguous.
2) Forward every field through every projection/copy: when a new request/response field is added, verify all downstream event copies and runtime conversions preserve it (including “pending_*”/projector paths).
3) Expose RPC operations consistently: operations used by clients must be registered/available through the public hub/client surface; otherwise runtime behavior can break or silently diverge.
4) Carry explicit identity/scope tokens: prefer passing an explicit scope/account token through snapshots/calls to prevent accidental account switching or reliance on repeated implicit checks.
5) Use self-describing interfaces in client code: avoid positional booleans in function signatures; prefer an options object (e.g. `{ refresh: true, userInitiated: true }`).
6) Pin and normalize API versions/URLs: when calling external services, use the correct versioned endpoints and normalize paths (trailing slashes, optional prefixes) to avoid environment-specific breakage.

Example (options object instead of boolean flags):
```ts
// before (ambiguous)
load(true, true)

// after (self-describing)
load({ refresh: true, userInitiated: true })
```