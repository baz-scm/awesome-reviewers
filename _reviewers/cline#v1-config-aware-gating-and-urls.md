---
title: Config-aware gating and URLs
description: All user-visible actions/links that depend on configuration (feature
  flags, environment/base URL, connectivity/credentials) must be driven by *resolved
  configuration state* and built consistently via centralized helpers.
repository: cline/cline#v1
label: Configurations
language: TSX
comments_count: 2
repository_stars: 70862
---

All user-visible actions/links that depend on configuration (feature flags, environment/base URL, connectivity/credentials) must be driven by *resolved configuration state* and built consistently via centralized helpers.

- Gate UI/commands using the best-known availability signal at render/session start (don’t rely on feature flags alone). 
- Build environment-specific URLs (e.g., dashboard/privacy endpoints) through one centralized URL builder that applies the resolved base URL + attribution consistently.
- If the resolved config is unavailable/undefined, use explicit fallback behavior (e.g., production URL or a clearly disabled/hide state) rather than emitting undefined links that silently break buttons.
- Keep correctness/security checks at runtime for things that can change (e.g., dirty state, remote probing), even if you gated the UI up front.

Example pattern:
```ts
// Centralized builder: uses resolved config with safe fallback
function buildAppLink(params: { path: string; attribution?: string; baseUrl?: string }) {
  const base = params.baseUrl ?? process.env.APP_BASE_URL_FALLBACK ?? "https://app.cline.bot";
  const url = new URL(params.path, base);
  if (params.attribution) url.searchParams.set("client", params.attribution);
  return url.toString();
}

// UI gating: decide availability from resolved connectivity/config (not only a flag)
const canRun = featureFlagEnabled && githubConnectionStatus === "connected";

<button
  disabled={!canRun}
  onClick={async () => {
    // Runtime safety checks still required
    if (await isDirtyWorkingTree()) throw new Error("Working tree is dirty");
    if (!await canReachRemote()) throw new Error("Remote check failed");
    // ...run command
  }}
>
  Open Dashboard
</button>

const dashboardUrl = buildAppLink({
  path: "/dashboard",
  attribution: clientAttribution,
  baseUrl: resolvedBaseUrl,
});
```

Applying this reduces “works in one environment but not another” behavior, prevents undefined link/button states, and improves UX by showing users actions only when configuration indicates they can succeed.