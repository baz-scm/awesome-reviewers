---
title: Centralize configuration resolution
description: When a configuration value (base URL, API key source, remote repository,
  helper binary path, provider settings) can be derived from several places — environment
  variables, saved settings, provider overrides, or defaults — resolve it in exactly
  one shared function and have every call site use that function's result instead
  of re-implementing the lookup....
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70964
---

When a configuration value (base URL, API key source, remote repository, helper binary path, provider settings) can be derived from several places — environment variables, saved settings, provider overrides, or defaults — resolve it in exactly one shared function and have every call site use that function's result instead of re-implementing the lookup. Duplicated resolution logic drifts apart over time and produces user-visible bugs: a privacy-settings link opening production while the account call targeted staging because one code path read the provider `baseUrl` override and the other read `appBaseUrl` directly, or a Bedrock-style "non-key" environment variable being excluded in one onboarding check but not in another.

Apply these rules:
1. Put the resolution logic in a shared module (e.g. `@cline/shared`/`@cline/core`) and export a single function (e.g. `resolveClineAppBaseUrl(apiBaseUrl)`, `isProviderApiKeyEnv()`) that every consumer — CLI, desktop sidecar, webview — imports rather than re-deriving the value locally.
2. If the backing inputs (account, environment, provider) cannot change after process startup, resolve the value once at startup and store the resolved result (e.g. on a context object), rather than re-reading provider settings or environment variables on every call.
3. When multiple override sources exist (explicit env var, config file, saved setting, inferred default), define and document one precedence order, and use it consistently everywhere the value is needed — don't let one code path check `ORIGIN_ENV_VAR` first while another defaults straight to a config value.
4. When no override source matches a known mapping (e.g. a self-hosted or proxy backend with no declared environment), resolve to `undefined`/disabled rather than silently falling back to the wrong environment.

Example:
```ts
// shared/environment.ts
export function resolveClineAppBaseUrl(apiBaseUrl: string): string | undefined {
  return ENVIRONMENTS.find(e => matchesBaseUrl(e, apiBaseUrl))?.appBaseUrl; // undefined if unmatched
}

// at startup (desktop sidecar)
ctx.clineAppBaseUrl = resolveClineAppBaseUrl(resolveAccountApiBaseUrl(providerSettings));

// every consumer reuses the resolved value instead of re-deriving it
return ctx.clineAppBaseUrl;
```
This keeps every surface (CLI, desktop, webview) pointed at the same environment/config and prevents silent divergence when override sources are added or changed.