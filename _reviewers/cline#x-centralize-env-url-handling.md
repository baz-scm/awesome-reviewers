---
title: Centralize env URL handling
description: 'When UI/actions depend on environment/config (base URLs, backend overrides,
  account identity), standardize it:


  - Centralize all environment-dependent link construction in one “URL builder” that
  takes the resolved app base URL and applies consistent client attribution/paths
  across every account link.'
repository: cline/cline#x
label: Configurations
language: TSX
comments_count: 5
repository_stars: 70861
---

When UI/actions depend on environment/config (base URLs, backend overrides, account identity), standardize it:

- Centralize all environment-dependent link construction in one “URL builder” that takes the resolved app base URL and applies consistent client attribution/paths across every account link.
- Resolve the environment base URL once per app lifetime (during initial config/transport startup) and cache it; do not re-fetch it on account refresh/reconnect unless the initial lookup failed.
- Avoid scattering hardcoded production URLs alongside environment-aware links; if the base URL is unresolved, prefer a consistent fallback strategy (e.g., production fallback) rather than leaving some links hidden while others work.
- Gate actions/UI up front using the resolved config/state (not only a feature flag), so users discover missing prerequisites before they click/run; still keep necessary runtime validation (e.g., dirty state/remote checks).
- Keep privacy/account data-sharing preferences in the account area (not under unrelated settings like telemetry), and avoid adding context/plumbing solely to support duplicate links.

Example pattern (cached base + single builder):

```ts
// resolves once at startup
let cachedAppBaseUrl: string | undefined;
async function resolveAppBaseUrl(desktopClient: any) {
  if (cachedAppBaseUrl !== undefined) return cachedAppBaseUrl;
  try {
    cachedAppBaseUrl = await desktopClient.invoke<string>("get_cline_app_base_url");
  } catch {
    cachedAppBaseUrl = undefined;
  }
  return cachedAppBaseUrl;
}

function buildAppUrl(appBaseUrl: string | undefined, path: string) {
  const base = appBaseUrl ?? "https://app.cline.bot"; // consistent fallback
  return `${base}${path}`;
}

// usage: every link calls the same builder
async function onOpenDashboard(desktopClient: any, userId: string) {
  const base = await resolveAppBaseUrl(desktopClient);
  const url = buildAppUrl(base, `/user/${userId}/dashboard`);
  window.open(url, "_blank", "noopener");
}
```

Applying these rules prevents mixed-environment navigation, eliminates redundant config calls on refresh, and improves user discoverability for config-dependent actions.