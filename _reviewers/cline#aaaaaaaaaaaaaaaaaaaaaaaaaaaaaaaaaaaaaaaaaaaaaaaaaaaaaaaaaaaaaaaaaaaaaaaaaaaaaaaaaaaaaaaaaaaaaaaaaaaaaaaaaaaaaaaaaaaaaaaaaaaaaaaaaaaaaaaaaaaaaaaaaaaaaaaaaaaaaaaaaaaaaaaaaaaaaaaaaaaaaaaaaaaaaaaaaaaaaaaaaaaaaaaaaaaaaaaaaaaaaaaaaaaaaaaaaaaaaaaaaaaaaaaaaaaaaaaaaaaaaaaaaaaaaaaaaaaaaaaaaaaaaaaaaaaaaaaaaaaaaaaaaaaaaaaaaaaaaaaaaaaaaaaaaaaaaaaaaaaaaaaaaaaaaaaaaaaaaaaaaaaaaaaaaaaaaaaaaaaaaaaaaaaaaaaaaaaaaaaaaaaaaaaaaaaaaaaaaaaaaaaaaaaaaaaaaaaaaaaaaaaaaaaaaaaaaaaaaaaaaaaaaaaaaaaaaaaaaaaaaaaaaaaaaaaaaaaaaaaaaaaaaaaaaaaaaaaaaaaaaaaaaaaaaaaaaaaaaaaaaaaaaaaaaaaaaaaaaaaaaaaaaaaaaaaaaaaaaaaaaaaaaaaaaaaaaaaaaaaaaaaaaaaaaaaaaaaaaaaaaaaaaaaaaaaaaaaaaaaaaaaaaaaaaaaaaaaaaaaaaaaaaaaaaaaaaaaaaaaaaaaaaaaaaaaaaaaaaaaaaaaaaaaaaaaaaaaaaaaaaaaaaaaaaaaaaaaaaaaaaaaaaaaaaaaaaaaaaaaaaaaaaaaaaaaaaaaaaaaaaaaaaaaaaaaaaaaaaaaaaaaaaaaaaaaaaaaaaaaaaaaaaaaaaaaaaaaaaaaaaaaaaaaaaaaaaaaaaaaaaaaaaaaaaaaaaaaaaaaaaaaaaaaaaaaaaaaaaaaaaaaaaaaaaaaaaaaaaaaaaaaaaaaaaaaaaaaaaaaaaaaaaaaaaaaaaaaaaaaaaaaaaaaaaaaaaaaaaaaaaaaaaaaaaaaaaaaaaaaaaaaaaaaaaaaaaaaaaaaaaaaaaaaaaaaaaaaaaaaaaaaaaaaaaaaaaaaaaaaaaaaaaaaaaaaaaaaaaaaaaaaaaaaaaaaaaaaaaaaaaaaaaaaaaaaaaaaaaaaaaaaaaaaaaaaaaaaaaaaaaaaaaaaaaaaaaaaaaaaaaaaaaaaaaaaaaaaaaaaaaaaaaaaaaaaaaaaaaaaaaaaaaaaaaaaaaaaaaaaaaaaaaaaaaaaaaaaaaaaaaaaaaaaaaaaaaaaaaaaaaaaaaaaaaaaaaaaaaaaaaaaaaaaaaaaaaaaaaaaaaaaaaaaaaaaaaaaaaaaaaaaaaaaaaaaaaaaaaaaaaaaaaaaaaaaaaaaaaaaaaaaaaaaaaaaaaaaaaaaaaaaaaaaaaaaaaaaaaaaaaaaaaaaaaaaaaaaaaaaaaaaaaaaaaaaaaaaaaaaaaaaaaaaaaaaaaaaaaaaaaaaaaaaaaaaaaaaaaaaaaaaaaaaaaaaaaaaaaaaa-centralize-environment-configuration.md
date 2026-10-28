---
title: Centralize environment configuration
description: 'Environment-specific values (base URLs, backend endpoints, feature-dependent
  links) must be resolved through a single centralized function/provider rather than
  hardcoded or re-derived ad hoc in each component. Concretely:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70965
---

Environment-specific values (base URLs, backend endpoints, feature-dependent links) must be resolved through a single centralized function/provider rather than hardcoded or re-derived ad hoc in each component. Concretely:

1. Avoid hardcoding environment URLs (e.g. production domains) in individual views. Instead, route every environment-dependent link through one builder so all consumers (dashboard, usage, billing, onboarding, privacy settings, etc.) automatically respect the configured environment, including proxy/self-hosted backends.

```ts
// Good: single source of truth
const dashboardUrl = buildClineAppUrl(clineAppBaseUrl, "/dashboard");
const usageUrl = buildClineAppUrl(clineAppBaseUrl, "/usage");

// Bad: hardcoded per-call
const dashboardUrl = "https://app.cline.bot/dashboard";
```

2. Resolve environment configuration once per app lifetime (e.g., at startup/transport connection), and cache it. Since the backend/environment doesn't change at runtime, don't re-fetch or reload this value on every unrelated refresh (e.g., account refresh). Only retry the lookup if the initial resolution failed (e.g., on reconnect), not on every subsequent operation.

3. When gating features or commands via feature flags or cached config/manifest data, treat that state as a UX hint only — it can be used to show/hide UI or display friendly unavailable messages, but it must not be treated as the authoritative check for access or safety. Required runtime validations (e.g., connection checks, remote state checks, permission checks) must still be performed at execution time, independent of the cached flag.

Following this pattern prevents inconsistent environments across links, redundant network calls, and security gaps where cached config is mistaken for real-time authorization.</description>
