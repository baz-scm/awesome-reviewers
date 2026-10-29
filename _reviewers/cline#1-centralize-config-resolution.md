---
title: Centralize config resolution
description: 'When a value depends on environment, overrides, or precedence rules
  (base URLs, remotes, directories, feature flags), resolve it in exactly one authoritative
  place and have every consumer use that resolved value instead of re-deriving it
  with separate fallback logic. Divergent resolution paths drift silently and are
  a common source of bugs: one path picked...'
repository: cline/cline#1
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 71024
---

When a value depends on environment, overrides, or precedence rules (base URLs, remotes, directories, feature flags), resolve it in exactly one authoritative place and have every consumer use that resolved value instead of re-deriving it with separate fallback logic. Divergent resolution paths drift silently and are a common source of bugs: one path picked up a staging override while a sibling path independently re-read the default environment config and opened production; a repo-remote selector in one module used different fallback rules than a similar selector elsewhere, risking a push target that didn't match what was displayed.

Concretely:
- Prefer resolving once at startup (or at the point an override is accepted) and storing the result on context/config, rather than recomputing it on every call. If the backend/account/provider can't change after startup, there's no need for a refresh lifecycle — resolve once and expose the field.
- Export one shared helper (e.g. `resolveAppBaseUrl(apiBaseUrl)`) that every call site imports, instead of letting each site independently combine environment config and override settings. If a resolved input doesn't map to anything known, fail safe (e.g. hide a link or disable a feature) rather than guessing a default that could point at the wrong environment.
- When a host process sets configuration only in its own memory (a module-level variable, provider settings), remember that subprocesses/worker sandboxes don't inherit it implicitly — explicitly copy the resolved value into `process.env` (or an equivalent explicit channel) so child processes observe the same configuration the host resolved.
- When multiple sources can supply the same setting (CLI flag, parent command flag, env var), resolve precedence in one place and test it explicitly, especially with frameworks that default negatable flags (e.g. Commander's `--no-mouse` defaults `mouse` to `true`) — use APIs like `getOptionValueSource` to distinguish "explicitly passed" from "default," so an unset flag doesn't silently override an environment variable fallback.
- Give test and build tooling an isolated environment (dedicated `HOME`, data dirs, discovery paths) so environment-variable-driven configuration in tests never reads or writes a developer's real config.

Example pattern to follow:
```ts
// shared/config.ts
export function resolveAppBaseUrl(apiBaseUrl: string): string | undefined {
  return ENVIRONMENTS.find(env => matchesBackend(env, apiBaseUrl))?.appBaseUrl;
}

// resolved once, not re-derived per call site
const apiBaseUrl = resolveAccountApiBaseUrl(providerSettings);
const appBaseUrl = resolveAppBaseUrl(apiBaseUrl); // undefined => hide the link, don't guess
```
Treat any second implementation of the same resolution logic as a bug waiting to diverge; unify it or make the single source of truth unmistakable.