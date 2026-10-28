---
title: Centralize environment config resolution
description: Environment-specific configuration (e.g. the app's base URL, which differs
  between production, proxy, and self-hosted setups) must be resolved through a single,
  centralized source rather than hardcoded in individual files or duplicated across
  call sites. Expose one provider/hook/builder (e.g. a `clineAppBaseUrl` from context,
  built via a...
repository: 'cline/cline

  '
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70942
---

Environment-specific configuration (e.g. the app's base URL, which differs between production, proxy, and self-hosted setups) must be resolved through a single, centralized source rather than hardcoded in individual files or duplicated across call sites. Expose one provider/hook/builder (e.g. a `clineAppBaseUrl` from context, built via a `get_cline_app_base_url` command) and have every consumer—links, onboarding, settings views—derive its values from that single source. Avoid mixing hardcoded constants (like a fixed production domain) with dynamically resolved values; if any single link bypasses the shared builder, it will silently point to the wrong environment for proxy/self-hosted users.

Resolve this configuration once, typically at startup/on first connection, and cache it for the app's lifetime instead of re-fetching it on every refresh or action. Only retry the lookup if the initial attempt failed (e.g., on reconnect), since runtime backend/environment switching is not a supported flow. If the value is unavailable, fail gracefully (e.g., hide the dependent UI) rather than falling back to a hardcoded default that may point to the wrong environment.

Example pattern:
```ts
// Resolved once in a shared context/provider
const clineAppBaseUrl = await desktopClient.invoke<string>("get_cline_app_base_url");

// All consumers build URLs through the same helper instead of hardcoding
const dashboardUrl = buildClineAppUrl(clineAppBaseUrl, "/dashboard");
const privacySettingsUrl = buildClineAppUrl(clineAppBaseUrl, "/privacy");
```
This ensures consistent, environment-aware behavior across the app and prevents configuration drift between features.