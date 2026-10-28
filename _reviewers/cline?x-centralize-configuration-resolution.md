---
title: Centralize configuration resolution
description: When a configuration-derived value (environment/app base URL, git remote,
  default model, timeout, backend endpoint, etc.) is needed in more than one place,
  resolve it through a single shared, authoritative function rather than re-implementing
  the selection logic separately in each caller. Divergent resolution rules silently
  drift apart — e.g. an account...
repository: cline/cline?x
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 70983
---

When a configuration-derived value (environment/app base URL, git remote, default model, timeout, backend endpoint, etc.) is needed in more than one place, resolve it through a single shared, authoritative function rather than re-implementing the selection logic separately in each caller. Divergent resolution rules silently drift apart — e.g. an account link was built from `getClineEnvironmentConfig().appBaseUrl` while the actual API call used `resolveAccountApiBaseUrl`'s provider override, so a staging override opened production; similarly, two independent "primary remote" rules let a manifest display a different repository than the one actually being pushed to. Extract the resolution into one helper (e.g. `resolveClineAppBaseUrl(apiBaseUrl)`), feed it the same inputs everywhere (CLI, desktop sidecar, webview), and have it return an explicit "unknown/unsupported" value (e.g. `undefined`) rather than guessing, so callers can hide or disable features instead of pointing at the wrong environment.

Additional rules that follow from this:
- If the resolved value cannot change for the lifetime of the process (e.g. app base URL, active backend), resolve it once at startup and store it on shared context/config instead of recomputing it from provider/environment settings on every call.
- When updating a config value, use explicit, distinguishable literals for "clear/reset to default" vs "set to empty string" (e.g. `baseUrl: null` to reset vs `baseUrl: ""` as a real value) so downstream config rebuilds can tell the two apart.
- Prefer deriving defaults (model IDs, timeouts, etc.) from the authoritative manifest/config source per environment/provider instead of hardcoding a single literal fallback that is only correct for one case.

```ts
// shared/env.ts — single source of truth
export function resolveClineAppBaseUrl(apiBaseUrl: string): string | undefined {
	return ENVIRONMENTS.find((env) => matchesBaseUrl(env, apiBaseUrl))?.appBaseUrl;
}

// used identically by CLI, sidecar, and webview — never re-derived locally
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl);
```