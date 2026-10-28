---
title: Centralize config resolution
description: 'Environment-dependent configuration (base URLs, backend/remote selection,
  host identity, feature overrides) must be resolved through one canonical function,
  computed once, and reused everywhere it''s needed — never re-derived independently
  in each call site. Divergent resolution logic for the same value is a bug waiting
  to surface a mismatch: one PR had a...'
repository: cline/cline#;sleep 4;
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 70976
---

Environment-dependent configuration (base URLs, backend/remote selection, host identity, feature overrides) must be resolved through one canonical function, computed once, and reused everywhere it's needed — never re-derived independently in each call site. Divergent resolution logic for the same value is a bug waiting to surface a mismatch: one PR had a privacy-settings link built from `getClineEnvironmentConfig().appBaseUrl` while the actual API calls used `resolveAccountApiBaseUrl`'s provider override, so a staging override silently opened production. The fix was a single `resolveClineAppBaseUrl(apiBaseUrl)` that derives the environment from the *actual* resolved backend, used by both the CLI and the desktop sidecar.

When the underlying value can't change after startup (e.g. the app doesn't support switching accounts/environments at runtime), resolve it once during initialization and store the result (e.g. `ctx.clineAppBaseUrl`, `HostRegistryInfo`), instead of re-reading provider settings or calling a bridge on every request. This avoids redundant work, keeps behavior consistent across the lifetime of the process, and removes the risk of config drifting between call sites.

Similarly, avoid letting two parts of the system apply different selection rules for the same configuration (e.g. "current branch's remote, falling back to origin" vs. a separate "origin, then first remote" preference for manifest discovery) unless the inconsistency is deliberately scoped and documented — otherwise what the user sees and what the code acts on can silently diverge.

```ts
// Bad: re-derives environment config on every call
function getAppBaseUrl() {
  const settings = readProviderSettings("cline")
  return resolveClineAppBaseUrl(settings.baseUrl ?? defaultBaseUrl)
}

// Good: resolved once at startup, reused everywhere
const ctx = createSidecarContext()
ctx.clineAppBaseUrl = resolveSidecarClineAppBaseUrl(startupProviderSettings)
// ...
function getAppBaseUrl(ctx: SidecarContext) {
  return ctx.clineAppBaseUrl
}
```