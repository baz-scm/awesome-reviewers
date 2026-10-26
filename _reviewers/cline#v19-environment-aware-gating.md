---
title: Environment-aware gating
description: When behavior or navigation depends on environment configuration (feature
  flags, app base URL, cloud enablement) and prerequisite runtime state (auth/remote
  connectivity, dirty state), make availability and links consistent and derived from
  the right sources.
repository: cline/cline#v19
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70885
---

When behavior or navigation depends on environment configuration (feature flags, app base URL, cloud enablement) and prerequisite runtime state (auth/remote connectivity, dirty state), make availability and links consistent and derived from the right sources.

Apply this as:
1) Centralize env-dependent URL/action construction
- Build all account/settings links through a single URL builder that uses the resolved app base URL (and attribution), so self-host/proxy environments don’t accidentally route users to production.
- Ensure there’s a defined fallback strategy when the resolved base URL is unavailable (don’t silently hide actions).

2) Gate UI availability using resolved config + prerequisite state (before execution)
- Don’t show/enable commands solely from a feature flag. Also incorporate prerequisite signals available at session start (e.g., workspace git metadata) or from the cloud service (e.g., GitHub connection state).
- Still perform authoritative runtime validation when the action executes (e.g., dirty workspace checks, `ls-remote`).

3) Keep account identity separate from environment configuration; avoid duplicated settings entries
- Derive privacy/account links from the user data within the Account view rather than publishing account identity/derived links through context just to support duplicates.
- Keep telemetry toggles vs account privacy/data-sharing actions in their correct UI surfaces.

Example pattern (env URL builder + gated visibility):
```ts
function buildAppUrl(baseUrl: string | undefined, path: string) {
  // central place for env base URL + attribution
  return baseUrl ? `${baseUrl}${path}` : undefined;
}

function isActionAllowed({ featureEnabled, gitRemoteKnown, cloudGitHubConnected }: {
  featureEnabled: boolean;
  gitRemoteKnown: boolean;
  cloudGitHubConnected: boolean;
}) {
  // gate up-front using available prerequisite state
  return featureEnabled && gitRemoteKnown && cloudGitHubConnected;
}

// On render: show/hide based on isActionAllowed(...)
// On click: still re-check dirty state / ls-remote / etc.
```