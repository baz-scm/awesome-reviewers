---
title: Centralize environment config
description: Never hardcode environment-specific values (base URLs, endpoints, API
  keys) at individual call sites. Resolve each value once through a single shared
  accessor/builder and have every consumer go through it, so behavior stays consistent
  across proxy, self-hosted, and production backends. For example, instead of six
  buttons each hardcoding `app.cline.bot`,...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70984
---

Never hardcode environment-specific values (base URLs, endpoints, API keys) at individual call sites. Resolve each value once through a single shared accessor/builder and have every consumer go through it, so behavior stays consistent across proxy, self-hosted, and production backends. For example, instead of six buttons each hardcoding `app.cline.bot`, build one `dashboardUrl`/`clineAppBaseUrl` helper and route every link (dashboard, usage, credits, privacy settings, onboarding) through it; if the value can't be resolved, hide the dependent UI rather than silently falling back to a default environment.

Resolve configuration that is fixed for the app's lifetime (environment, backend URL) once at startup, not on every refresh or reconnect. Only retry the initial lookup if it failed; a successful resolution should be cached and reused, since runtime backend switching isn't a supported flow.

When a configuration value is backed by multiple stores (e.g., a legacy secret store and a newer provider-config store), updates and clears must keep all of them in sync, and this should be covered by a regression test that writes/clears the value and asserts every store and the effective merged config agree.