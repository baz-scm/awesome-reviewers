---
title: Centralize env links
description: When behavior depends on environment/config (feature availability, app
  base URLs, privacy/account links), ensure it’s derived in one place and applied
  consistently.
repository: CLINE/CLINE
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70837
---

When behavior depends on environment/config (feature availability, app base URLs, privacy/account links), ensure it’s derived in one place and applied consistently.

Apply these rules:
- Build env/config-derived URLs (dashboard, usage, privacy, etc.) via a single shared URL builder using the resolved app base URL + attribution.
- Don’t mix identity-derived data into global config/account contexts. If a link can be derived from data fetched inside the target view (e.g., user), derive it there; keep environment configuration (e.g., `clineAppBaseUrl`) separate.
- Gate feature actions up front using known prerequisite/config state (e.g., workspace manifest, exposed connection state). Still perform correctness checks at runtime (e.g., dirty checks / remote verification).
- Avoid duplicating the same settings/privacy entry across sections; keep account/data-sharing preferences in the Account view (not telemetry/general settings) to prevent duplicated dependencies.

Example pattern (centralized builder):
```ts
function buildAccountUrl(appBaseUrl: string | undefined, path: string) {
  const base = appBaseUrl ?? 'https://app.cline.bot'; // or a deterministic fallback
  return `${base}${path}`;
}

// In AccountView:
const dashboardUrl = buildAccountUrl(clineAppBaseUrl, '/dashboard');
const privacyUrl = buildAccountUrl(clineAppBaseUrl, `/privacy?user=${user.id}`);
```
This prevents mixed environments, avoids undefined links/hidden actions, and keeps configuration and identity responsibilities properly separated.