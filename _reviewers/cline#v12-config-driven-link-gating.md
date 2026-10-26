---
title: Config-driven link gating
description: 'Apply configuration management rules consistently across UI actions,
  links, and settings:


  - Separate environment configuration from account identity: expose env-only values
  (e.g., app base URL) via configuration, but keep account-derived data (e.g., user/privacy/apply
  actions) inside Account components instead of global context.'
repository: cline/cline#v12
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70872
---

Apply configuration management rules consistently across UI actions, links, and settings:

- Separate environment configuration from account identity: expose env-only values (e.g., app base URL) via configuration, but keep account-derived data (e.g., user/privacy/apply actions) inside Account components instead of global context.
- Centralize environment-dependent link building: use one URL builder that applies the resolved base URL + attribution consistently to every account link; ensure a deterministic fallback when the resolved base is missing (so self-hosted/proxy deployments don’t silently hide buttons or send users to mixed environments).
- Gate user-facing capabilities with both feature flags and state/config known up front: don’t rely on feature flags alone. If the product already has session-start workspace manifest info or cloud can expose connection state, use that to show/hide actions early.
- Still enforce correctness at runtime: even if you gate in the UI, validate critical preconditions at execution time (e.g., dirty state, remote reachability).
- Keep account/privacy preferences in the Account area, not under unrelated settings categories (e.g., telemetry toggles), and avoid adding account dependencies to unrelated settings sections.

Example (central URL builder + consistent fallback):
```ts
const prodBase = "https://app.cline.bot";

function buildAccountUrl(path: string, envBase?: string) {
  const base = envBase ?? prodBase; // deterministic fallback
  const url = new URL(path, base);
  // optionally apply attribution/client query params here
  // url.searchParams.set("client", "desktop");
  return url.toString();
}

// Usage: every account link uses the same builder
const dashboardUrl = buildAccountUrl("/dashboard", clineAppBaseUrl);
```