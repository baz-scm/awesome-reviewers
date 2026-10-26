---
title: Consistent Config-Driven UI
description: When behavior and links depend on environment configuration or external
  prerequisites, use config-driven resolution consistently across UI and actions.
repository: cline/cline#v5
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70864
---

When behavior and links depend on environment configuration or external prerequisites, use config-driven resolution consistently across UI and actions.

Apply these rules:
1) Single source of truth for env-specific URLs: resolve the configured app base URL once (with any attribution/client parameters) and build all related account/dashboard/privacy links through the same URL builder. Avoid mixing env-resolved links with hardcoded production URLs.
2) Define fallback behavior: if the environment app base URL cannot be resolved, ensure link behavior is deterministic (e.g., fall back to production or a well-defined default) rather than leaving links undefined and hiding buttons.
3) Gate UI using prerequisites, not only feature flags: when an action requires GitHub connectivity/remote state, reflect that availability before the user can trigger it (using manifest/session state and/or service-exposed connection status). Still perform authoritative runtime checks for dirty state and remote validation.
4) Keep context boundaries clean: don’t propagate derived account-identity data or view-specific URLs through shared contexts if the destination view can fetch/derive them. Expose environment configuration separately from account identity/config.

Example (central URL builder + deterministic link):
```ts
function buildAppUrl(baseUrl: string | undefined, path: string, clientAttribution: string) {
  const resolvedBase = baseUrl ?? "https://app.cline.bot"; // explicit fallback
  return `${resolvedBase}${path}?client=${encodeURIComponent(clientAttribution)}`;
}

// In the view
const dashboardUrl = buildAppUrl(clineAppBaseUrl, "/dashboard", attributionClient);

// Render links/buttons using the computed URL (never leave undefined)
<a href={dashboardUrl}>Open dashboard</a>
```

Outcome: users won’t see “enabled” actions that fail later, links won’t drift across environments, and shared state/context remains minimal and correctly scoped to configuration vs identity.