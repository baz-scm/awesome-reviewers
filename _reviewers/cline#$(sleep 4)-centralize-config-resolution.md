---
title: Centralize config resolution
description: When a setting can be derived from multiple sources (environment config,
  provider overrides, CLI flags, env vars, stored settings), resolve it in exactly
  one shared helper and have every consumer call that helper instead of re-deriving
  the value with its own logic. Duplicated resolution logic drifts apart over time
  — e.g. one code path preferred a provider...
repository: cline/cline#$(sleep 4)
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 70978
---

When a setting can be derived from multiple sources (environment config, provider overrides, CLI flags, env vars, stored settings), resolve it in exactly one shared helper and have every consumer call that helper instead of re-deriving the value with its own logic. Duplicated resolution logic drifts apart over time — e.g. one code path preferred a provider `baseUrl` override while another used `appBaseUrl` from environment config, so a staging override silently produced a link into production. Fix this class of bug by extracting a single `resolveX()` function that all callers (webview, sidecar, CLI) share.

For values that don't change during a session (app base URL, startup flags), resolve them once at startup and store the result in context/config rather than recomputing them on every call or every refresh — this avoids both drift between call sites and unnecessary repeated work.

When a value can come from several layers (e.g. a subcommand flag, a root flag, an environment variable), define an explicit precedence order, document it, and verify end-to-end that it actually reaches the consuming code — not just that it's declared on some entry point. A flag added only to a test-only command builder, or resolved with the option's effective value instead of its *source*, can silently fail to override the env fallback. Add a test exercising every combination (flag present/absent at each level, env var set/unset) to lock in the intended precedence.

Finally, normalize identifiers consistently between the write and read paths of stored configuration (e.g. lowercase provider IDs before persisting and before looking them up) so that a save and a later read/delete always target the same record; a case mismatch can leave a provider "successfully" disabled while its credentials are still stored, or silently create an unreachable duplicate entry.

Example of centralizing resolution instead of duplicating it:
```ts
// shared helper, single source of truth
export function resolveClineAppBaseUrl(apiBaseUrl: string): string | undefined {
  return ENVIRONMENTS.find(e => trimSlash(e.apiBaseUrl) === trimSlash(apiBaseUrl))?.appBaseUrl;
}

// every caller uses the same helper against the same resolved apiBaseUrl
const apiBaseUrl = resolveAccountApiBaseUrl(providerSettings);
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // undefined for proxy/self-hosted
```