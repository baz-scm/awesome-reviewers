---
title: Env-consistent link building
description: 'When code is driven by environment configuration or feature flags, make
  behavior deterministic and consistent across the UI.


  Apply these rules:

  1) Centralize env-dependent URL/link generation'
repository: cline/cline#v3
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70863
---

When code is driven by environment configuration or feature flags, make behavior deterministic and consistent across the UI.

Apply these rules:
1) Centralize env-dependent URL/link generation
- Create a single URL builder that takes the resolved environment base URL (and any attribution/client parameters) and use it for all related links in a view (dashboard, usage, credits, privacy).
- Avoid duplicating “app base” logic or hardcoded production URLs in some paths.

2) Never allow “unresolved config” to silently hide functionality
- If the environment base URL cannot be resolved, prefer a defined fallback (e.g., production) so buttons/links still work.
- Avoid leaving links undefined (which often results in hidden buttons and inconsistent behavior across environments).

3) Keep environment config separate from account identity state
- Do not place env/config-derived values inside account/user contexts when they don’t change with account refresh.
- Derive user-dependent links (e.g., privacy URL) inside the component that fetches the user; expose env base URL separately via configuration utilities/providers.

4) Gate feature-flag affordances with prerequisites
- Don’t show or offer an action based on the feature flag alone. Gate up front using cheap, readily-available prerequisites (e.g., connection state known at session start).
- Still re-validate expensive/authoritative conditions at run time (e.g., dirty state, remote checks).

Example (pattern):
```ts
function buildDashboardUrl({ baseUrl, attribution, pathname }: {
  baseUrl: string | undefined;
  attribution: string;
  pathname: string;
}) {
  const resolvedBase = baseUrl ?? "https://app.cline.bot"; // defined fallback
  return new URL(`/dashboard/${pathname}?attribution=${encodeURIComponent(attribution)}`, resolvedBase).toString();
}

// In the view: use the same builder for every related button/link.
const dashboardUrl = buildDashboardUrl({ baseUrl: clineAppBaseUrl, attribution, pathname: "overview" });
```

This standard prevents cross-environment link inconsistencies, avoids broken/hidden actions when configuration is missing, and keeps config-driven concerns cleanly separated from account/user synchronization.