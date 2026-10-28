---
title: Centralize configuration sources
description: Avoid hardcoding environment-specific values or duplicating configuration
  settings across the codebase. Instead, route all reads and writes through a single,
  centralized resolver so behavior stays consistent across proxy, self-hosted, and
  production environments, and so every consumer of a setting sees the same value.
repository: cline/cline#&&sleep 4
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70980
---

Avoid hardcoding environment-specific values or duplicating configuration settings across the codebase. Instead, route all reads and writes through a single, centralized resolver so behavior stays consistent across proxy, self-hosted, and production environments, and so every consumer of a setting sees the same value.

Concretely:
- Resolve environment-dependent values (base URLs, endpoints, etc.) through one builder function used everywhere they're needed, rather than hardcoding constants in individual components. For example, instead of each button constructing its own URL with a hardcoded `app.cline.bot`, pass the resolved config through a shared `buildDashboardUrl(path)` helper so every link (dashboard, usage, credits, privacy settings, onboarding) honors the configured environment. If the base URL can't be resolved, hide the dependent UI rather than silently falling back to a hardcoded production value.
- When a setting (e.g., an API key) is stored in more than one place (legacy secret store and a newer structured config store), write and clear it through a single effective-config path that updates both stores atomically, so they never fall out of sync. Add a regression test that seeds both stores with different values, performs a write/clear, and asserts both stores and the effective config agree.
- Don't duplicate a configuration entry or toggle across multiple settings views/sections. Keep each setting scoped to the view that owns it, and remove duplicate entries (and any extra module dependencies they introduce) rather than maintaining the same setting in two places.