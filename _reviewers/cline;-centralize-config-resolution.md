---
title: Centralize config resolution
description: Avoid scattering environment-specific or secret values (base URLs, API
  keys, feature endpoints, etc.) across multiple components or stores. Resolve such
  configuration once, in a single provider/context, and expose it through one shared
  accessor/builder that every consumer uses, rather than letting individual views
  hardcode values or build their own...
repository: cline/cline;
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70964
---

Avoid scattering environment-specific or secret values (base URLs, API keys, feature endpoints, etc.) across multiple components or stores. Resolve such configuration once, in a single provider/context, and expose it through one shared accessor/builder that every consumer uses, rather than letting individual views hardcode values or build their own URLs/paths. For example, instead of each button in an account view constructing its own `app.cline.bot/...` link, add a single `buildDashboardUrl(path)`-style helper backed by one resolved `clineAppBaseUrl`, and route every link through it so proxy/self-hosted/staging environments are respected consistently.

Treat configuration that is fixed for the app's lifetime (environment, backend base URL, etc.) as immutable after the first successful resolution: fetch it once at startup, retry only if the initial lookup failed, and don't re-fetch it on unrelated events like account refresh or reconnect—this avoids redundant network calls and prevents transient failures from clearing a previously-resolved value.

When a config value is mirrored across multiple stores (e.g., a legacy secret store and a newer structured config file), ensure writes, updates, and clears are applied atomically to all stores so they never diverge; add a regression test that seeds both stores with different values, performs a write/clear, and asserts both stores and the effective merged config end up consistent.</description>
</invoke>
