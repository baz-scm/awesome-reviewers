---
title: Environment-aware gating and links
description: 'Standardize how the app uses environment config and feature flags so
  users see correct options up front and never end up in the wrong environment.


  Apply this when adding/removing actions, buttons, or outbound links:'
repository: cline/cline#v25
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70891
---

Standardize how the app uses environment config and feature flags so users see correct options up front and never end up in the wrong environment.

Apply this when adding/removing actions, buttons, or outbound links:
1) Gate UI availability using required state, not just a feature flag
- If an action requires external connectivity/identity (e.g., GitHub connection, repo metadata, cloud handoff eligibility), compute the availability from the workspace manifest and/or backend-reported connection state.
- Still validate preconditions at runtime (e.g., dirty state, `ls-remote`)—but avoid hiding the reason behind a click.

2) Centralize environment-specific URL construction
- Build all account/account-view-related outbound URLs (dashboard, privacy, credits, org links, etc.) via one shared builder that applies the resolved app base URL and client attribution consistently.
- Eliminate hardcoded production URLs in views that are expected to work in proxy/self-hosted environments.

3) Separate environment config from account identity
- Don’t stuff identity-derived URLs/data into global account context just to support duplicated UI links. Expose environment configuration (like app base URL) separately, and derive account-specific links inside the view that owns the fetched user.

4) Define fallback behavior when env config is missing
- If the resolved app base URL is unavailable/undefined, do not silently hide buttons or return undefined links; fall back to a safe default (e.g., production) or show an explicit disabled state with rationale.

Example (shared builder + fallback):

```ts
const getAppBaseUrl = (): string => {
  return process.env.CLINE_APP_BASE_URL ?? "https://app.cline.bot";
};

function buildAccountLink(path: string, attribution: string) {
  const baseUrl = getAppBaseUrl();
  return new URL(path, baseUrl).toString() + `?client=${encodeURIComponent(attribution)}`;
}

// In AccountView: all links route through the same builder.
const dashboardUrl = buildAccountLink("/dashboard", attribution);
const privacyUrl = buildAccountLink("/privacy", attribution);
```

Outcome: consistent environment routing, fewer broken/hidden UI paths, and clearer user experience around feature-flagged capabilities.