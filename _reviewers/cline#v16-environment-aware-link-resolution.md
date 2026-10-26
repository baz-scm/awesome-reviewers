---
title: Environment-aware link resolution
description: 'Use environment configuration as a first-class input for UI capabilities
  and links: resolve app base URLs/targets centrally, gate actions up front based
  on resolved configuration/connection state, keep environment config separate from
  account identity, and prefer backend-provided availability/reasons (using current
  settings only as fallback for...'
repository: cline/cline#v16
label: Configurations
language: TSX
comments_count: 5
repository_stars: 70882
---

Use environment configuration as a first-class input for UI capabilities and links: resolve app base URLs/targets centrally, gate actions up front based on resolved configuration/connection state, keep environment config separate from account identity, and prefer backend-provided availability/reasons (using current settings only as fallback for legacy/partial hosts).

How to apply:
- Centralize env-dependent link building: one “URL resolver/builder” that takes the resolved `appBaseUrl` (from environment) and applies consistent client attribution.
- Gate UI buttons/commands using resolved state: don’t rely only on a feature flag; hide/disable when required prerequisites (e.g., GitHub connection/remote state) are already known, then still re-check at execution time.
- Separate concerns in state/context:
  - Put environment-only values (e.g., `appBaseUrl`) in a config provider.
  - Avoid pushing identity-specific derived URLs (e.g., privacy link) through account context just to support duplicate UI locations.
- Prefer source-of-truth from the backend:
  - If the backend returns an explicit reason (e.g., checkpoints disabled), use it.
  - Only use the current local setting when the backend omits the reason (legacy compatibility).

Example pattern (central resolver + fallback):
```ts
type LinkContext = { appBaseUrl?: string; clientAttribution?: string };

function buildDashboardUrl({ appBaseUrl, clientAttribution }: LinkContext) {
  // Fallback to production (or a defined default) so self-host/proxy cases don’t hide buttons.
  const base = appBaseUrl ?? "https://app.cline.bot";
  return `${base}/dashboard?client=${encodeURIComponent(clientAttribution ?? "web")}`;
}

// Usage: build all account links via the same resolver
const dashboardUrl = buildDashboardUrl({ appBaseUrl, clientAttribution });
```

This prevents mixed environments, duplicate link logic, and “undefined link -> hidden button” behavior, while keeping UI consistent with current runtime configuration and backend-reported availability.