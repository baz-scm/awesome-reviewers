---
title: Config-based Links & Actions
description: When code exposes environment- or account-dependent actions/links, wire
  them through a single configuration-aware mechanism and avoid mixing unrelated configuration
  sources.
repository: cline/cline#v6
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70864
---

When code exposes environment- or account-dependent actions/links, wire them through a single configuration-aware mechanism and avoid mixing unrelated configuration sources.

Apply these rules:
1) Centralize environment-specific URL generation
- Use one URL builder that applies the resolved environment/base URL and any attribution consistently across all links.
- If the environment value is unresolved, provide a stable fallback (e.g., production) instead of returning `undefined` and hiding buttons.

2) Separate environment config from account-derived identity
- Keep global/shared context limited to environment configuration that does not change with account refresh.
- Derive account-identity URLs (e.g., privacy/app-specific dashboard) inside the account UI that already fetches the user; avoid publishing account-derived links in global context.

3) Pre-check availability beyond feature flags
- Don’t rely solely on a feature flag to present actions.
- Gate (disable/hide) up front using cheap known state (workspace manifest) and/or cloud-provided connection availability; still perform authoritative runtime checks (e.g., dirty state / `ls-remote`) when the action runs.

Example pattern (URL builder + fallback):
```ts
type Urls = { dashboard: string; privacy: string };

function buildUrls(appBaseUrl: string | undefined): Urls {
  const base = appBaseUrl ?? 'https://app.cline.bot'; // fallback
  return {
    dashboard: `${base}/dashboard`,
    privacy: `${base}/privacy`,
  };
}

// In Account UI:
const urls = buildUrls(clineAppBaseUrl);
// Use urls.dashboard / urls.privacy consistently for every button.
```