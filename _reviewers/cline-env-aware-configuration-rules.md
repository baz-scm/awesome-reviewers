---
title: Env-Aware Configuration Rules
description: When an implementation depends on environment-specific configuration
  (e.g., app base URL) or capability flags, apply configuration consistently and gate
  user actions with real state.
repository: Cline/Cline
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70840
---

When an implementation depends on environment-specific configuration (e.g., app base URL) or capability flags, apply configuration consistently and gate user actions with real state.

**Standards**
1) **Centralize environment-specific URL building**
- Build all account-related links (dashboard/privacy/etc.) through a single helper that uses the resolved environment base URL and any required attribution/client IDs.
- Avoid mixing env-resolved links with hardcoded production URLs.

2) **Don’t gate solely on feature flags**
- If a feature is enabled by flag, still gate the UI/availability using cheap, already-known state (workspace manifest session start) and/or cloud-provided capability (e.g., GitHub connection status) so users don’t discover missing prerequisites only after clicking.
- Keep **runtime** validation for correctness (e.g., dirty state checks, remote reachability like `ls-remote`).

3) **Separate env/config from account identity in shared state**
- Shared context should expose **environment/config-only** values (e.g., `clineAppBaseUrl`) but not account-derived fields just to support duplicated UI.
- Derive account-dependent URLs inside the owning view/component (e.g., `AccountView`) rather than publishing them in global context.

**Example pattern (centralized builder + local derivation)**
```ts
// config-only value belongs in context/provider
export const clineAppBaseUrl: string | undefined = /* env resolution */ undefined;

function buildAppUrl(baseUrl: string | undefined, path: string) {
  if (!baseUrl) return undefined;
  return `${baseUrl}${path}`; // extend with attribution/client attribution if needed
}

function AccountView() {
  const { clineAppBaseUrl } = useAccount();
  const user = /* fetch user inside this view */ null;

  const privacyUrl = user
    ? buildAppUrl(clineAppBaseUrl, `/privacy?uid=${user.id}`)
    : undefined;

  // render privacy button only when privacyUrl is resolved
}
```

Apply this standard to keep links correct across environments (self-hosted/proxy setups), prevent confusing UX from incomplete gating, and reduce unnecessary cross-component coupling.