---
title: Contract-first API design
description: 'When designing or consuming client/server APIs, keep the contract explicit
  and prevent duplicate logic/types from drifting.


  Apply this standard:

  - **Single source of truth:** If the backend persists/owns a value, the UI should
  display it directly—avoid re-adding client fallbacks that recreate the same logic.'
repository: aaif-goose/goose
label: API
language: TypeScript
comments_count: 5
repository_stars: 51876
---

When designing or consuming client/server APIs, keep the contract explicit and prevent duplicate logic/types from drifting.

Apply this standard:
- **Single source of truth:** If the backend persists/owns a value, the UI should display it directly—avoid re-adding client fallbacks that recreate the same logic.
- **No contract drift:** Don’t export additional request/type wrappers that duplicate the method’s already-type-checked signature unless they add real behavior/guarantees.
- **Clear protocol boundaries:** Distinguish **wire-format** types from **internal/extended** types and document mappings intentionally.
- **Typed surfaces > generic fallbacks:** Provide a dedicated typed callback/API for each notification/method; use a generic dispatcher only for untyped/escape-hatch cases.
- **Centralize API access patterns:** If multiple call sites repeat `getClient()` + thin wrappers, centralize into a shared utility/hook to keep calling semantics consistent.

Example patterns:
- Don’t reintroduce UI fallback when the server is authoritative:
```ts
export function getSessionDisplayName(session: Session): string {
  return session.name || DEFAULT_CHAT_TITLE;
}
```
- Avoid exporting a redundant request type when the method signature already validates:
```ts
// Prefer relying on GooseClient.initialize(...) typing
// instead of maintaining GooseInitializeRequest that can diverge.
```
- Keep notifications typed and route generically only as fallback:
```ts
export interface GooseExtNotifications {
  unstable_sessionUpdate?: (n: GooseSessionNotification_unstable) => Promise<void>;
}
```
