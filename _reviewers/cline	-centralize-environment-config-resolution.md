---
title: Centralize environment config resolution
description: Environment-dependent configuration values (base URLs, API keys, feature
  flags) must be resolved and written through a single canonical accessor/builder,
  never hardcoded or duplicated across multiple call sites or storage locations. Scattered
  constants (e.g. a hardcoded production URL repeated in several buttons) silently
  diverge from configured...
repository: "cline/cline\t"
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70947
---

Environment-dependent configuration values (base URLs, API keys, feature flags) must be resolved and written through a single canonical accessor/builder, never hardcoded or duplicated across multiple call sites or storage locations. Scattered constants (e.g. a hardcoded production URL repeated in several buttons) silently diverge from configured environments like proxy or self-hosted backends; route every consumer through one function so overrides apply everywhere consistently.

When a config value is backed by more than one store (e.g. a legacy secret plus a newer provider-config store), every write or clear must update all backing stores atomically so the effective configuration never drifts out of sync—add a regression test that writes/clears the value and asserts both stores agree.

Resolve configuration at the appropriate point in the lifecycle instead of redundantly. If a value is fixed for the app's lifetime (e.g. backend base URL), fetch it once at startup and retry only on initial-lookup failure—don't re-fetch it on every unrelated refresh or reconnect, since that adds needless work without reflecting any real change.

Example pattern:
```ts
// bad: hardcoded per call site
const dashboardUrl = "https://app.cline.bot/dashboard";
const usageUrl = "https://app.cline.bot/usage"; // drifts for self-hosted/proxy

// good: single builder, used everywhere
const buildAccountUrl = (path: string) => `${clineAppBaseUrl ?? DEFAULT_BASE_URL}${path}`;
const dashboardUrl = buildAccountUrl("/dashboard");
const usageUrl = buildAccountUrl("/usage");
```