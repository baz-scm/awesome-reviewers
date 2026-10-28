---
title: Centralize environment config resolution
description: Environment-specific values (base URLs, API keys, feature endpoints,
  etc.) must come from a single, authoritative source rather than being hardcoded
  or duplicated across the codebase. When a value depends on the active environment
  or backend, build it through one shared resolver/builder function that all call
  sites use, so every consumer stays consistent...
repository: cline/cline#|sleep 4
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70979
---

Environment-specific values (base URLs, API keys, feature endpoints, etc.) must come from a single, authoritative source rather than being hardcoded or duplicated across the codebase. When a value depends on the active environment or backend, build it through one shared resolver/builder function that all call sites use, so every consumer stays consistent and automatically picks up proxy, self-hosted, or alternate-environment configurations instead of silently falling back to a hardcoded default (e.g., `app.cline.bot`).

Resolve such configuration once during startup/initialization, not repeatedly on every refresh or reconnect. If the initial lookup fails, retry on reconnect, but once resolved successfully, reuse the cached value for the lifetime of the session — the backend/environment is fixed for the app's lifetime and does not need re-resolution on unrelated events like `refreshAccount`.

When a configuration value is persisted in multiple stores (e.g., a legacy secret store and a newer structured config file), all writes/clears must update every store atomically and consistently. Add regression tests that set divergent values across stores, perform a write/clear, and assert both stores and the effective merged config end up consistent.

Example pattern:
```ts
// Single builder used by every link/consumer
const dashboardUrl = buildClineUrl(clineAppBaseUrl, "/dashboard");
const privacySettingsUrl = buildClineUrl(clineAppBaseUrl, "/privacy");

// Resolve once at startup, cache for the session
useEffect(() => {
  if (!clineAppBaseUrl) {
    loadAppBaseUrl(); // retried only on reconnect if it previously failed
  }
}, []);
```
This avoids environment drift, inconsistent links/behavior across features, and stale or partially-updated configuration state.</description>
