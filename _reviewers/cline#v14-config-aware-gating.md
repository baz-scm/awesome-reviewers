---
title: Config-aware gating
description: 'When configuration or environment-specific behavior controls what a
  user can access (features, commands, external links, UI actions), ensure the code
  is *configuration-aware end-to-end*: (1) gate availability using the real underlying
  state (not only a feature flag), (2) centralize environment-specific logic behind
  a single builder, (3) keep...'
repository: cline/cline#v14
label: Configurations
language: TSX
comments_count: 5
repository_stars: 70876
---

When configuration or environment-specific behavior controls what a user can access (features, commands, external links, UI actions), ensure the code is *configuration-aware end-to-end*: (1) gate availability using the real underlying state (not only a feature flag), (2) centralize environment-specific logic behind a single builder, (3) keep identity/account-derived values derived close to where the identity is fetched, and (4) still validate conditions at runtime with safe fallbacks.

Apply it like this:
- Up-front gating: hide/disable actions or buttons unless required state is known to be available (e.g., GitHub connected + remote present). Feature flags alone are not sufficient; the workspace manifest / cloud service should provide the availability signal.
- Single source of truth for environment URLs/links: build all account-related outbound links (dashboard, privacy, credits/org routes, etc.) through one environment-aware URL builder, with deterministic fallback behavior if the env base URL is missing.
- Separation of concerns in state/context:
  - Environment configuration (e.g., app base URL) may live in a long-lived provider.
  - Account-identity-linked values (e.g., privacy URL that depends on the fetched user) should be derived in the Account view itself rather than synchronized via a shared account context.
- Runtime safety + preferences: even if gated up front, still perform the necessary runtime checks (e.g., dirty-state/remote checks) before executing. Also respect user/environment preferences (e.g., `prefers-reduced-motion`) unless an explicit prop overrides.

Example pattern (centralized env builder + graceful fallback):
```ts
function buildAppUrl(path: string, appBaseUrl?: string) {
  const base = appBaseUrl ?? "https://app.cline.bot"; // deterministic fallback
  return `${base}${path}`;
}

// use everywhere to avoid mixed environments
const dashboardUrl = buildAppUrl("/dashboard", clineAppBaseUrl);
const privacyUrl = buildAppUrl("/privacy", clineAppBaseUrl);
```

This prevents “hidden until clicked” failures, avoids inconsistent environment routing (especially for proxy/self-hosted setups), and reduces brittle coupling between account identity and global configuration state.