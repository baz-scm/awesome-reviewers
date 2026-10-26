---
title: Use env-aware configuration
description: 'When behavior or UI depends on configuration (feature flags, env-specific
  base URLs, app base resolution, integrations), ensure you:

  1) Gate actions/controls using the *effective* capability computed from resolved
  configuration/state (not just a feature flag). Still run required repository/permission
  checks at execution time.'
repository: cline/cline#v27
label: Configurations
language: TSX
comments_count: 2
repository_stars: 70892
---

When behavior or UI depends on configuration (feature flags, env-specific base URLs, app base resolution, integrations), ensure you:
1) Gate actions/controls using the *effective* capability computed from resolved configuration/state (not just a feature flag). Still run required repository/permission checks at execution time.
2) Generate all external/internal links through a single centralized env-aware URL builder so the resolved app base URL, client attribution, and environment selection are consistent. Avoid hardcoded production URLs and define consistent fallback behavior when base URL resolution is missing.

Example (pattern):

```ts
// 1) Up-front gating (effective capability)
function computeChatComposerAvailability({
  cloudAgentsEnabled,
  githubConnected,
  hasGitRemote,
}: {
  cloudAgentsEnabled: boolean;
  githubConnected: boolean;
  hasGitRemote: boolean;
}) {
  return cloudAgentsEnabled && githubConnected && hasGitRemote;
}

const cloudHandoffAvailable = computeChatComposerAvailability({
  cloudAgentsEnabled,
  githubConnected, // from resolved session/cloud state
  hasGitRemote,    // from session manifest/startup data
});

// Still validate at run time before performing the action.
async function runCloudHandoffSafely() {
  // runtime checks remain mandatory
  // e.g., dirty state check, ls-remote/permission check, etc.
}

// 2) Centralized URL builder (consistent environment links)
function buildDashboardUrl({
  appBaseUrl,   // resolved env-specific base
  clientId,     // attribution
  path,
  fallbackBaseUrl, // optional consistent fallback
}: {
  appBaseUrl?: string;
  fallbackBaseUrl: string;
  clientId: string;
  path: string;
}) {
  const base = appBaseUrl ?? fallbackBaseUrl;
  const url = new URL(path, base);
  url.searchParams.set('client', clientId);
  return url.toString();
}

const dashboardUrl = buildDashboardUrl({
  appBaseUrl: clineAppBaseUrl,
  fallbackBaseUrl: 'https://app.cline.bot', // or configured fallback
  clientId,
  path: '/dashboard',
});
```

Result: users see correct controls before they click, and all account/dashboard links consistently follow the resolved environment (including proxies/self-hosted) with predictable fallbacks.