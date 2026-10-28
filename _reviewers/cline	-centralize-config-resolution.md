---
title: Centralize config resolution
description: When a value depends on environment or runtime configuration (base URLs,
  active environment, selected git remote, host name, etc.), resolve it in exactly
  one place and have every consumer reuse that resolved value instead of re-implementing
  the selection/resolution logic independently. Divergent copies of the same resolution
  rule silently drift and produce...
repository: "cline/cline\t"
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 70947
---

When a value depends on environment or runtime configuration (base URLs, active environment, selected git remote, host name, etc.), resolve it in exactly one place and have every consumer reuse that resolved value instead of re-implementing the selection/resolution logic independently. Divergent copies of the same resolution rule silently drift and produce inconsistent behavior across surfaces (e.g., a staging `baseUrl` override being honored by one code path but not by another, which opened production privacy settings instead of staging).

Prefer resolving configuration once, as early as possible (e.g., at process/context startup), and store the result on shared context/state rather than recomputing it on every call. If the underlying settings cannot change after startup, there is no need to re-derive the value on each request — pass the already-resolved value down (e.g., `ctx.clineAppBaseUrl`, `HostRegistryInfo`) instead of adding a parallel lookup or refresh lifecycle.

Example of the fix pattern:
```ts
// Bad: each caller re-derives the environment from its own rules
const link = getClinePrivacySettingsUrl(path, getClineEnvironmentConfig().appBaseUrl);

// Good: resolve once, from the same backend URL that was actually used
const apiBaseUrl = resolveAccountApiBaseUrl(settings);
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // undefined if backend isn't a known environment
const link = getClinePrivacySettingsUrl(path, appBaseUrl);
```

When adding a new config-dependent code path, first check whether an existing resolver/shared value already answers the question; extend or reuse it rather than writing a second rule that can fall out of sync.