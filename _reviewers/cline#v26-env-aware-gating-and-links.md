---
title: Env-aware gating and links
description: 'When behavior, actions, or links depend on feature flags, account state,
  or environment configuration, make the dependency explicit and consistent:


  - **Gate up front**: If a feature-flagged command/button requires prerequisites
  (e.g., GitHub connection), hide/disable it before execution using cheap state available
  at render/session start. Still...'
repository: cline/cline#v26
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70893
---

When behavior, actions, or links depend on feature flags, account state, or environment configuration, make the dependency explicit and consistent:

- **Gate up front**: If a feature-flagged command/button requires prerequisites (e.g., GitHub connection), hide/disable it before execution using cheap state available at render/session start. Still **re-validate at run time** (e.g., dirty state, `ls-remote`, etc.).
- **Centralize environment-specific URLs**: Use a single URL builder for all links that should follow the resolved app base URL/attribution. Avoid mixing environment-aware links with hardcoded production URLs. Provide a **defined fallback** (e.g., production) when the app base URL can’t be resolved, so UI doesn’t become silently unavailable.
- **Separate env config from account-derived data**: Keep environment configuration (like `clineAppBaseUrl`) in shared config context if it’s stable; but don’t publish account-identity/link derivations (like privacy settings URLs) into global context if they’re only needed in one account-related view—compute them where used to prevent unnecessary synchronization and coupling.

Example pattern:
```ts
// Centralized builder (single source of truth for env-aware links)
function buildAppUrl(path: string, appBaseUrl?: string) {
  const base = appBaseUrl ?? "https://app.cline.bot"; // fallback
  return new URL(path, base).toString();
}

// Up-front gating
const canRun = cloudFlagEnabled && githubConnectionKnown;

<button disabled={!canRun} onClick={async () => {
  // run-time validation still required
  await ensureNotDirty();
  await ensureRemoteListingWorks();
  await runCommand();
}}>
  Run
</button>
```
Apply this to UI surfaces and settings/links so users get consistent destinations and predictable availability across environments, proxies, and self-hosted setups.