---
title: Resolve configs once
description: 'When code depends on environment/service configuration (base URLs, environment-specific
  routes, feature availability signals), resolve and apply it consistently:'
repository: cline/cline#v29
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70893
---

When code depends on environment/service configuration (base URLs, environment-specific routes, feature availability signals), resolve and apply it consistently:

- Resolve app/environment configuration once (startup or initial transport handshake), then reuse it across account refreshes and reconnects. Avoid re-fetching config inside “refresh account” flows.
- Centralize environment-aware URL building in one place and ensure *all* account/settings links use the same resolved base URL (no mixed hardcoded production URLs).
- Keep global/shared context limited to true app-wide config. Derive account/user-specific links inside the view that fetches the user; don’t duplicate identity-derived URLs into shared context.
- For feature/command UI, gate visibility using cheap upfront state (e.g., known connection/manifest info), but still perform correctness checks at run time (e.g., dirty state, `ls-remote`).

Example pattern:

```ts
// Provider: resolve once
const [appBaseUrl, setAppBaseUrl] = useState<string | undefined>();
useEffect(() => {
  desktopClient.invoke<string>("get_cline_app_base_url")
    .then(setAppBaseUrl)
    .catch(() => setAppBaseUrl(undefined));
}, []);

// Centralized builder: all links share environment
function buildDashboardUrl(appBaseUrl: string | undefined, path: string) {
  if (!appBaseUrl) return undefined;
  return new URL(path, appBaseUrl).toString();
}

// In AccountView: derive links after fetching user
const dashboardUrl = buildDashboardUrl(appBaseUrl, `/dashboard/${user?.id ?? ""}`);
```

This prevents inconsistent environments, reduces reload churn, and avoids context synchronization bugs.