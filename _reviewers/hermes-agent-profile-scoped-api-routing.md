---
title: Profile-scoped API routing
description: All profile-scoped routing must use the mechanism your IPC/bridge/router
  actually consumes (e.g., an outer request field or a `...profileScoped()` wrapper).
  Do not attempt to “scope” routing by placing `profile` inside nested request bodies
  that the backend simply binds/forwards, or by passing `profile` only as a query
  param unless the bridge explicitly...
repository: nousresearch/hermes-agent
label: API
language: TypeScript
comments_count: 7
repository_stars: 221948
---

All profile-scoped routing must use the mechanism your IPC/bridge/router actually consumes (e.g., an outer request field or a `...profileScoped()` wrapper). Do not attempt to “scope” routing by placing `profile` inside nested request bodies that the backend simply binds/forwards, or by passing `profile` only as a query param unless the bridge explicitly treats it as a routing key.

Apply the rule:
- Prefer a single, reusable client wrapper (e.g., `profileScoped()`) at the API call site.
- Ensure any facade helpers (filesystem, session ops, plugin calls) forward the explicit profile override through the same routing-aware path as other calls.
- For destructive or state-changing operations, never bypass the profile-aware facade.
- For operations that imply cross-profile/multi-backend movement, define destination routing explicitly; don’t assume a payload field will route to the destination backend if the router only uses the outer profile.

Example pattern:
```ts
return window.hermesDesktop.api<Response>({
  ...profileScoped(), // routing key understood by the bridge/router
  path: '/api/audio/speak',
  method: 'POST',
  body: { text }, // backend binding; don’t rely on body nesting for routing
});
```