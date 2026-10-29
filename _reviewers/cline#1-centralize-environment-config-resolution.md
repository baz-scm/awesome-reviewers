---
title: Centralize environment config resolution
description: Environment-specific configuration (base URLs, backend endpoints, feature
  toggles) must be resolved through a single, shared mechanism rather than hardcoded
  or duplicated across components. Build one helper/builder that resolves values like
  the app base URL and apply it consistently to every consumer (dashboard, usage,
  billing, onboarding, connector links,...
repository: cline/cline#1
label: Configurations
language: TSX
comments_count: 3
repository_stars: 71024
---

Environment-specific configuration (base URLs, backend endpoints, feature toggles) must be resolved through a single, shared mechanism rather than hardcoded or duplicated across components. Build one helper/builder that resolves values like the app base URL and apply it consistently to every consumer (dashboard, usage, billing, onboarding, connector links, etc.) so all parts of the UI point to the same configured environment (production, proxy, self-hosted). Avoid hardcoding environment-specific constants in individual components; route them through the shared resolver instead.

Resolve this configuration once, typically at startup, since the backend/environment is fixed for the app's lifetime. Don't re-fetch or reset it on every refresh, reconnect, or state change—only retry the initial lookup if it failed. For example:

```ts
// contexts/account-context.tsx
const loadAppBaseUrl = useCallback(async () => {
  try {
    setClineAppBaseUrl(await desktopClient.invoke<string>("get_cline_app_base_url"));
  } catch {
    // retried only on reconnect if the initial lookup failed
  }
}, []);

// resolved once on mount / first successful transport connection,
// NOT inside refreshAccount or other frequently-called handlers
```

```ts
// utils/dashboard-url.ts
export function buildDashboardUrl(baseUrl: string | undefined, path: string) {
  if (!baseUrl) return undefined; // hide the link rather than falling back to a hardcoded prod URL
  return `${baseUrl}${path}`;
}
```

Also avoid introducing config/account dependencies into unrelated settings sections just to surface a link or value—keep configuration-driven UI in the view that owns that configuration, and let other views reuse the same resolver if they need it.