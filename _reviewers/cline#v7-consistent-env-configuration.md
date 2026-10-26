---
title: Consistent Env Configuration
description: 'When behavior or links depend on environment/runtime configuration,
  generate them centrally and in the correct scope.


  **Rules**

  1) **Centralize env-aware URLs**: Build account/view URLs through a single resolver
  (e.g., using the resolved app base URL + attribution) so all links stay on the same
  environment.'
repository: cline/cline#v7
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70865
---

When behavior or links depend on environment/runtime configuration, generate them centrally and in the correct scope.

**Rules**
1) **Centralize env-aware URLs**: Build account/view URLs through a single resolver (e.g., using the resolved app base URL + attribution) so all links stay on the same environment.
2) **Don’t leak derived account identity into global context**: Keep identity-derived links (like privacy settings) computed inside the view that already fetches the user; use context for stable environment config only.
3) **Provide deterministic fallbacks**: If the resolved app base URL is unavailable, choose a clear fallback (e.g., production) rather than leaving links undefined/hidden—especially for self-hosted or proxied setups.
4) **Respect runtime/user preferences**: For UI behavior that varies by runtime signals (e.g., `prefers-reduced-motion`), default to those preferences while letting explicit props override.

**Example (URL builder + scope separation)**
```ts
// env-only config in context
type AppConfig = { clineAppBaseUrl?: string };

function buildAppUrl(config: AppConfig, path: string) {
  const base = config.clineAppBaseUrl ?? "https://app.cline.bot"; // deterministic fallback
  return `${base}${path}`;
}

function AccountView({ appConfig }: { appConfig: AppConfig }) {
  // user-derived values computed locally (no identity link in global context)
  const user = useFetchUser();
  const dashboardUrl = user
    ? buildAppUrl(appConfig, `/u/${user.id}/dashboard`)
    : undefined;

  return <a href={dashboardUrl}>Open dashboard</a>;
}
```

Applying these rules prevents mixed-environment links, duplicate UI/actions driven by mis-scoped data, and broken behavior when environment configuration is incomplete.