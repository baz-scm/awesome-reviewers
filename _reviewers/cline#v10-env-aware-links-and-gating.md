---
title: Env-aware links and gating
description: 'When implementing UI/commands that depend on configuration (feature
  flags, environment base URLs, account connection state), ensure:


  1) Configuration-driven enablement (early)'
repository: cline/cline#v10
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70869
---

When implementing UI/commands that depend on configuration (feature flags, environment base URLs, account connection state), ensure:

1) Configuration-driven enablement (early)
- Don’t rely on a feature flag alone to decide whether an action will work.
- Use cheap, already-available session/workspace config/state to show/hide or enable/disable the command/link up front.
- Still perform definitive runtime checks before executing (e.g., dirty state, remote accessibility).

2) Single source of truth for environment-dependent URLs
- Create one URL builder that takes the resolved environment base URL and applies any required attribution.
- Ensure all account links in a view use that builder (avoid hardcoded production URLs).
- If the environment base URL is unresolved, provide a clear fallback (e.g., production) rather than leaving links undefined/hidden.

3) Separate env config from account-derived identity
- Keep environment configuration (e.g., `clineAppBaseUrl`) in shared context if it is stable and non-account-specific.
- Derive account-privacy and user-specific links inside the component that fetches the user; don’t publish account-derived values globally just to support duplicated UI.

Example (centralized builder + fallback):
```ts
const APP_BASE_FALLBACK = 'https://app.cline.bot';

function buildAccountUrl(params: {
  baseUrl?: string;
  path: string;
  attribution?: string;
}) {
  const base = params.baseUrl ?? APP_BASE_FALLBACK;
  const url = new URL(params.path, base);
  if (params.attribution) url.searchParams.set('attribution', params.attribution);
  return url.toString();
}

// Usage: every account link uses the same builder
const dashboardUrl = buildAccountUrl({
  baseUrl: clineAppBaseUrl,
  path: '/dashboard',
});
```

Apply these rules to reduce inconsistent environments, prevent broken/hidden links, avoid unnecessary context coupling, and make feature availability match the user’s real configuration state.