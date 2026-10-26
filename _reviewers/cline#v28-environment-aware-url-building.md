---
title: Environment-Aware URL Building
description: All environment-sensitive URLs (account dashboards, privacy settings,
  attribution-dependent links) must be built consistently from configuration, and
  account-derived data should not be globally synchronized just to support duplicated
  UI.
repository: cline/cline#v28
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70893
---

All environment-sensitive URLs (account dashboards, privacy settings, attribution-dependent links) must be built consistently from configuration, and account-derived data should not be globally synchronized just to support duplicated UI.

Apply this standard:
1) Use one URL builder for account links
- Centralize base-URL resolution (from env/config) and client attribution so every link in a given view uses the same logic.
- Avoid hardcoded production endpoints for links that should respect self-hosted/proxy environments.

2) Handle missing/undefined config predictably
- If the resolved app base URL is unavailable, ensure buttons/links either fall back to a safe default (if intended) or use a clear, consistent behavior rather than silently hiding functionality.

3) Keep privacy/account preference links in the Account UI
- Don’t place account data-sharing/privacy actions under unrelated sections (e.g., telemetry/general settings). When you centralize the UI, remove any now-unneeded account-derived fields from shared contexts.

4) Separate configuration from identity in shared state
- Expose environment configuration (e.g., app base URL) via context if it’s not tied to account refresh.
- Compute account-identity-derived links (privacy/dashboard URLs) inside the Account view from fetched user data, rather than pushing identity/link values into the global context.

Example (pattern):
```ts
// config-aware URL builder (single source of truth)
function buildAccountUrl(opts: {
  baseUrl?: string;
  path: string;
  attributionClient?: string;
}) {
  const base = opts.baseUrl;
  if (!base) return undefined; // or a deliberate fallback

  const url = new URL(opts.path, base);
  if (opts.attributionClient) url.searchParams.set('client', opts.attributionClient);
  return url.toString();
}

// In AccountView: derive links from identity fetch + config
const dashboardUrl = buildAccountUrl({
  baseUrl: clineAppBaseUrl,
  path: '/dashboard',
  attributionClient: applyClientAttribution,
});

// Avoid pushing privacy/link URLs into global context unless they are truly config-only.
```

This prevents environment mismatch (production vs configured base), reduces duplicated UI wiring, and keeps configuration/state separation clean.