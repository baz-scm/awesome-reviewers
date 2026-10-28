---
title: Centralize environment config
description: Environment- or deployment-specific values (base URLs, API keys, feature
  endpoints) must be resolved through a single, centralized source of truth rather
  than hardcoded or duplicated across components. When a setting can vary by environment
  (production, self-hosted, proxy) or is stored in more than one place, build one
  resolver/builder function that every...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70964
---

Environment- or deployment-specific values (base URLs, API keys, feature endpoints) must be resolved through a single, centralized source of truth rather than hardcoded or duplicated across components. When a setting can vary by environment (production, self-hosted, proxy) or is stored in more than one place, build one resolver/builder function that every consumer calls, and route every write through the canonical config path so all backing stores stay in sync.

Practical guidance:
- Resolve environment-dependent config (e.g. app base URL) once at startup/connection time and cache it; don't refetch it on every unrelated refresh. Only retry if the initial resolution failed.
- Expose a single builder for derived values (e.g. dashboard/privacy links) that all call sites use, instead of letting some links use the resolved value while others keep hardcoded production constants. If the base value can't be resolved, hide/disable dependent UI rather than silently falling back to a hardcoded default.
- When a setting has multiple underlying stores (e.g. legacy secret storage vs. a newer provider-config file), never write to just one. Use the existing unified config-write path so every store is updated and read consistently, and add a regression test that verifies writes/clears propagate to all stores.

Example (bad): scattering `app.cline.bot` across six buttons, or writing an API key directly to a legacy secret store while a newer `providers.json` path exists.

Example (good):
```ts
// one builder used by every link
const dashboardUrl = buildClineUrl(clineAppBaseUrl, "/dashboard");

// one path for writing config that keeps all stores in sync
await setProviderSetting("lmstudio", "apiKey", value); // updates StateManager + providers.json
```