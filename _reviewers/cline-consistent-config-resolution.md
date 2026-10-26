---
title: Consistent Config Resolution
description: When decisions depend on environment/provider/backend/config, resolve
  them once using shared, centralized helpers, then pass the resolved value downstream.
  Avoid duplicated “mini re-resolvers” that can drift.
repository: Cline/Cline
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70840
---

When decisions depend on environment/provider/backend/config, resolve them once using shared, centralized helpers, then pass the resolved value downstream. Avoid duplicated “mini re-resolvers” that can drift.

Practical rules:
- **Use one source of truth**: prefer helpers in shared packages (core/llms) so UI/runtime/build logic can’t disagree.
- **Resolve once per lifecycle**: if the app doesn’t support switching backends/environments after startup, compute at startup and reuse (don’t recompute on refresh).
- **Make precedence explicit**: implement consistent ordering for inputs (e.g., explicit CLI flag vs env vs derived defaults). For negatable flags, don’t rely on raw option values—use the option’s source to decide.
- **Honor explicit overrides**: when a caller supplies an override, it should win over derived defaults.
- **Isolate tests from ambient config**: set HOME/config/discovery paths (or equivalent) in smoke/tests so external developer/session settings can’t affect results.

Example (precedence + negatable CLI):
```ts
// Use option value source so negatable defaults don't clobber env fallback.
const mouse = (authCmd.getOptionValueSource("mouse") === "cli")
  ? authCmd.opts().mouse
  : undefined;

const useMouse = input.mouse ?? (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```
Example (resolve once + pass through):
```ts
// Resolve backend->app base URL once (with shared helper), then build links from that exact value.
const apiBaseUrl = resolveBackendOnce(/* provider + env */);
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // shared
return { privacySettingsUrl: appBaseUrl ? `${appBaseUrl}/privacy` : undefined };
```