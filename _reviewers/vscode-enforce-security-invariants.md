---
title: Enforce security invariants
description: Security decisions (sandboxing, allow/deny access, and token attachment)
  must remain correct across time, async races, and concurrent policy contributions.
repository: microsoft/VSCode
label: Security
language: TypeScript
comments_count: 10
repository_stars: 194303
---

Security decisions (sandboxing, allow/deny access, and token attachment) must remain correct across time, async races, and concurrent policy contributions.

Apply this standard:
1) Re-evaluate enablement per execution
- Do not capture “enabled”/policy state once and assume it stays valid. Re-check the authoritative policy/enablement at invocation time, and add tests for false→true (and revocation) transitions.

2) Preserve policy provenance and enforce deny-wins
- If a native/policy lock exists, preserve that provenance; don’t downgrade containment because a forwarded/effective value loses “locked” semantics.
- When multiple runtimes/sources contribute policy, aggregate with deny-wins semantics per owner and remove each runtime’s contribution when it disposes.

3) Prevent TOCTOU with cancellation/epochs
- For eligibility checks that involve async network/work, never allow stale in-flight results to update shared state (cache/UI/manifest). Cancel prior work or use an epoch/token so superseded generations cannot mutate status.

4) Cancel in-flight UI-triggered security operations on revocation
- If access becomes “none”/revoked, ensure pending searches/snapshots are canceled so they can’t still fetch/compute results.

5) Never leak credentials/bearer tokens
- Only attach Authorization/Cookie for strict same-origin HTTPS endpoints.
- For token-bearing requests, avoid redirect-chasing that could forward the Authorization header to a different origin; treat unexpected 3xx as failure.

6) Clear security markers per interaction
- If an interaction tags a bypass/escape marker, ensure later confirmations cannot reuse it accidentally. Stamp/clear markers for every new confirmation path, and add bypass→allow-once→re-confirmation regression tests.

Minimal example pattern (epoch + cancellation + safe token target):
```ts
const ctsRef = new MutableDisposable();
let epoch = 0;

async function resolveAccess(nowUrl: string) {
  const token = (ctsRef.value = new CancellationTokenSource()).token;
  const myEpoch = ++epoch;

  // 1) start async eligibility check, pass token so it can abort
  const result = await eligibilityRequest({ url: nowUrl, cancellationToken: token });
  if (token.isCancellationRequested || myEpoch !== epoch) return; // TOCTOU guard

  // 2) only now mutate shared state
  if (result.eligible) updateManifest();
  else markDenied();
}

function authorizationHeader(targetUrl: string): Record<string, string> {
  if (!isSameSecureOrigin(targetUrl, marketplaceEligibilityOrigin)) return {};
  return { Authorization: `Bearer ${token}` };
}
```
