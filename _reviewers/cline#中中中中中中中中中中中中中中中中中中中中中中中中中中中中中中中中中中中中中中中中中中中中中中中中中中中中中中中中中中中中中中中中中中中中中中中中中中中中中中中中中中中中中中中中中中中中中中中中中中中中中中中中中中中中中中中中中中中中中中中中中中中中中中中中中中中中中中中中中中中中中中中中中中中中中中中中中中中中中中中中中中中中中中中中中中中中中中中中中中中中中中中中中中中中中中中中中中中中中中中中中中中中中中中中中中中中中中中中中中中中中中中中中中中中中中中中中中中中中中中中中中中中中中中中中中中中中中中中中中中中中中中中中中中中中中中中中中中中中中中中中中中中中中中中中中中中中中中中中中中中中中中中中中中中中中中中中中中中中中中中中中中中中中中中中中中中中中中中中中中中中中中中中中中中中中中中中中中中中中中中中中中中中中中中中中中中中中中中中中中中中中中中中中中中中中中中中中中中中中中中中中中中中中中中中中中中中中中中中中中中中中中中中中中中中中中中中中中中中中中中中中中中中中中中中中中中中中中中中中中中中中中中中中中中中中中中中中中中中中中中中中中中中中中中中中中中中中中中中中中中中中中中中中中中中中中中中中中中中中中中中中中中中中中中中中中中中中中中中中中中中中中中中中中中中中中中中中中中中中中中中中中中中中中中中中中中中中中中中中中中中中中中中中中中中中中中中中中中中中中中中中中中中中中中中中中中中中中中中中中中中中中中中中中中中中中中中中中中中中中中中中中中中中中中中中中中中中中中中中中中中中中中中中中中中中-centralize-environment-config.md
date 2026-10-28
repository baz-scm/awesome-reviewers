---
title: Centralize environment config
description: Environment- or deployment-dependent values (base URLs, API keys, feature
  endpoints) must be resolved through a single, centralized builder/accessor rather
  than hardcoded or duplicated across components. Scattering constants like a production
  URL across many call sites makes it easy to miss environments such as proxy or self-hosted
  backends, producing...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70986
---

Environment- or deployment-dependent values (base URLs, API keys, feature endpoints) must be resolved through a single, centralized builder/accessor rather than hardcoded or duplicated across components. Scattering constants like a production URL across many call sites makes it easy to miss environments such as proxy or self-hosted backends, producing inconsistent behavior where some links/features respect the configured environment and others silently fall back to production.

Guidelines:
- Expose one function/hook that resolves the environment-specific value (e.g., `getClineAppBaseUrl()` / a `dashboardUrl` builder) and route every consumer through it instead of hardcoding constants like `app.cline.bot`.
- Resolve configuration that is fixed for the app's lifetime (e.g., backend/environment) once, at startup or connection time, and cache it. Don't re-fetch it on every refresh/reconnect; only retry if the initial lookup failed.
- If the resolved value is unavailable, hide or disable the dependent feature rather than falling back to a potentially wrong hardcoded default.
- When a setting is persisted in multiple places (e.g., a legacy secret store and a newer provider-config store), writes and reads must go through one abstraction that keeps all stores in sync, including clearing the value everywhere when it's unset.

Example pattern:
```ts
// single resolver, computed once
const clineAppBaseUrl = useMemo(() => resolveAppBaseUrl(sidecarEnv), [sidecarEnv]);

// all links/features derive from the same builder
const dashboardUrl = buildClineUrl(clineAppBaseUrl, "/dashboard");
const privacySettingsUrl = buildClineUrl(clineAppBaseUrl, user?.dataPrivacyPath);

// provider API key goes through one config path so both stores stay consistent
await providerConfig.setApiKey("lmstudio", value); // updates StateManager AND providers.json
```

This keeps every feature aligned with the configured environment, avoids stale or partially-updated configuration, and prevents regressions when new environments (proxy, self-hosted) are introduced.</description>
</invoke>
