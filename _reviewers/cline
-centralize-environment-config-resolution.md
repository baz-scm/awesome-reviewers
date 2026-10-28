---
title: Centralize environment-config resolution
description: 'Environment-dependent configuration (app/account base URLs, environment
  variable fallbacks, directory paths like `CLINE_DIR`) must be resolved through a
  single, shared, authoritative function rather than re-derived independently by each
  consumer. Divergent resolution logic is a recurring source of bugs: a privacy-settings
  link opened production instead of...'
repository: "cline/cline\r\n"
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70946
---

Environment-dependent configuration (app/account base URLs, environment variable fallbacks, directory paths like `CLINE_DIR`) must be resolved through a single, shared, authoritative function rather than re-derived independently by each consumer. Divergent resolution logic is a recurring source of bugs: a privacy-settings link opened production instead of staging because it read `getClineEnvironmentConfig().appBaseUrl` while account calls actually honored a provider `baseUrl` override; the CLI and TUI handled provider API-key environment-variable fallbacks differently until they shared one `isProviderApiKeyEnv()` helper; and `CLINE_DIR` was set only on a host module variable, so worker/subprocess sandboxes with their own environment never saw it.

Apply this by:
- Extracting one resolver (e.g. `resolveClineAppBaseUrl(apiBaseUrl)`, `isProviderApiKeyEnv()`) that every caller imports, instead of each call site reading raw env/config independently.
- For values that cannot change after startup (app environment, backend base URL), resolve once during initialization and store/pass the resolved value (e.g. set `ctx.clineAppBaseUrl` once in the sidecar context) rather than recomputing it on every request or account refresh.
- When configuration must cross a process/sandbox boundary, explicitly copy it onto that process's environment (e.g. copy `resolveClineDir()` into `CLINE_DIR` on a worker/subprocess's `env`); never assume a module-level variable is visible outside the host process.
- When a resolver can't map a value to any known environment (e.g. a self-hosted or proxy backend), fail safe — return `undefined`/hide the dependent feature — instead of defaulting to another environment.

```ts
// shared helper, used by every caller (CLI, desktop sidecar, webview)
export function resolveClineAppBaseUrl(apiBaseUrl: string): string | undefined {
  const env = ENVIRONMENTS.find((e) => matchesBackend(e, apiBaseUrl));
  return env?.appBaseUrl; // undefined for an unrecognized backend, not a guess
}

// resolved once at startup, not per call
ctx.clineAppBaseUrl = resolveSidecarClineAppBaseUrl(providerSettings);
```