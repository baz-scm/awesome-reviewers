---
title: Config-aware link generation
description: When code depends on configuration (environment or user/system preferences),
  derive it centrally and in the correct scope—don’t hardcode production values and
  don’t mix env-derived config with account/user state.
repository: cline/cline#v2
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70861
---

When code depends on configuration (environment or user/system preferences), derive it centrally and in the correct scope—don’t hardcode production values and don’t mix env-derived config with account/user state.

Apply:
- Environment-dependent URLs: use a single URL builder that resolves the configured app base URL + attribution for every link in a view; avoid scattered hardcoded endpoints and ensure links don’t silently diverge by environment.
- State/context boundaries: expose environment configuration separately from identity/account data; avoid pushing account-fetched/link-specific values into global/shared context when the view can derive them locally.
- Preference-driven UI behavior: default behaviors should follow configuration such as `prefers-reduced-motion`; allow explicit props to override.

Example pattern (centralized env-aware builder + preference-respecting behavior):
```ts
// Centralized: every link uses the same env-aware builder
const appBaseUrl = getConfiguredAppBaseUrl();
function buildDashboardUrl(path: string) {
  return `${appBaseUrl}${path}?client_attribution=${getClientAttribution()}`;
}

// Preference-respecting: follow prefers-reduced-motion unless explicitly overridden
function scrollToBottom({ behavior }: { behavior?: ScrollBehavior }) {
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches;
  const resolvedBehavior = behavior ?? (reduced ? 'auto' : 'smooth');
  window.scrollTo({ top: document.body.scrollHeight, behavior: resolvedBehavior });
}
```

Outcome: consistent behavior across environments and views, fewer synchronization bugs from misplaced state, and UI that respects user/system configuration by default.