---
title: Centralize environment configuration
description: Route all environment-dependent values (base URLs, API keys, feature
  endpoints) through a single resolver/builder instead of hardcoding them per call
  site. For example, replace scattered `app.cline.bot` literals with one `buildDashboardUrl(path)`
  helper so every link (dashboard, usage, billing, onboarding) automatically follows
  the configured environment,...
repository: cline/cline?ref=main
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70980
---

Route all environment-dependent values (base URLs, API keys, feature endpoints) through a single resolver/builder instead of hardcoding them per call site. For example, replace scattered `app.cline.bot` literals with one `buildDashboardUrl(path)` helper so every link (dashboard, usage, billing, onboarding) automatically follows the configured environment, including proxy and self-hosted backends; if the base value can't be resolved, hide the dependent UI rather than silently falling back to production.

Resolve configuration that is fixed for the app's lifetime (e.g., app base URL, backend environment) once at startup, not on every refresh/reconnect. Only retry the initial lookup if it failed; once resolved, cache and reuse it instead of re-fetching on unrelated events like `refreshAccount`.

When a setting is persisted in more than one place (e.g., a legacy secret store and a newer `providers.json`/config store), writes and clears must update all locations atomically so they never diverge — write through a single config-store API rather than updating one legacy path directly.