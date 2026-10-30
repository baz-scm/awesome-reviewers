---
title: Centralize environment configuration
description: Treat environment-specific configuration (base URLs, API keys, backend
  endpoints) as a single source of truth rather than duplicating or hardcoding it
  across the codebase. Build links and derived values (e.g., dashboard, usage, billing,
  privacy URLs) through one shared builder/resolver that applies the configured environment
  consistently, instead of...
repository: cline/cline#zzz-unlikely-123abc
label: Configurations
language: TSX
comments_count: 4
repository_stars: 71035
---

Treat environment-specific configuration (base URLs, API keys, backend endpoints) as a single source of truth rather than duplicating or hardcoding it across the codebase. Build links and derived values (e.g., dashboard, usage, billing, privacy URLs) through one shared builder/resolver that applies the configured environment consistently, instead of hardcoding production URLs in multiple components—this ensures proxy, self-hosted, and other environments behave correctly everywhere. Resolve configuration that is fixed for the app's lifetime (such as an app base URL) once at startup, with retry only on initial failure; do not re-fetch or recompute it on every refresh/reconnect cycle, since the backend/environment doesn't change at runtime. When a setting is represented in more than one store (e.g., a legacy secret store and a provider config store), writes and clears must update all of them atomically so the stores never drift out of sync. Finally, avoid placing the same configuration-dependent UI element (e.g., account/privacy links) in multiple unrelated settings sections—keep it co-located with its owning domain to prevent unnecessary cross-section dependencies and duplicate maintenance burden.

Example: instead of
```ts
const dashboardUrl = "https://app.cline.bot/dashboard";
const usageUrl = "https://app.cline.bot/usage";
```
use a single builder:
```ts
const buildAccountUrl = (path: string) => `${clineAppBaseUrl ?? DEFAULT_BASE_URL}${path}`;
const dashboardUrl = buildAccountUrl("/dashboard");
const usageUrl = buildAccountUrl("/usage");
```
and resolve `clineAppBaseUrl` once at app startup rather than inside `refreshAccount`.