---
title: Environment-aware feature gating
description: 'When adding environment-/account-dependent actions or links, follow
  a single-source-of-truth approach:


  1) Centralize environment-specific URL/config generation'
repository: cline/cline#v8
label: Configurations
language: TSX
comments_count: 5
repository_stars: 70867
---

When adding environment-/account-dependent actions or links, follow a single-source-of-truth approach:

1) Centralize environment-specific URL/config generation
- Use one builder/function that takes the resolved environment base URL (and any attribution/attribution params) and produces all related links (dashboard, privacy, usage, etc.).
- Avoid hardcoded production URLs inside the account/settings views.
- Provide a clear fallback when the environment base can’t be resolved, so UI doesn’t silently disappear.

2) Keep config scopes separate
- Environment configuration (e.g., app base URL) can live in app-level providers.
- Account-identity-derived values (e.g., privacy/consent links tied to a fetched user) should be derived inside the view/component that fetches/owns that user data—don’t “publish” identity-derived URLs into unrelated global contexts just to reuse a duplicate UI entry.
- Don’t duplicate the same action in multiple settings areas under different categories.

3) Gate UI up front with real capability, but still validate at runtime
- Don’t show actions based only on a feature flag.
- Compute “can show/enable” from cheap, already-available state (e.g., workspace manifest/git URL/branch; cloud/GitHub connection state if available).
- Still re-check required conditions at execution time (e.g., dirty repo state, remote accessibility) to handle stale/changed state.

Example pattern (illustrative):
```ts
// Centralized environment-aware URL builder
function buildAccountLink(appBaseUrl: string | undefined, path: string) {
  if (!appBaseUrl) return undefined; // caller can decide fallback/hidden
  return `${appBaseUrl}${path}`;
}

// View derives identity-dependent links locally
function AccountView({ user }: { user: ClineAccountUser | null }) {
  const appBaseUrl = useAppBaseUrl();
  const privacyUrl = user ? buildAccountLink(appBaseUrl, `/privacy?uid=${user.id}`) : undefined;
  return privacyUrl ? <a href={privacyUrl}>Privacy settings</a> : null;
}

// Up-front gating (cheap state) + runtime validation at execution
function ConnectRepoAction({ canUse }: { canUse: boolean }) {
  const disabled = !canUse;
  async function onClick() {
    // runtime re-checks (dirty state, remote accessibility)
    const ok = await checkRepoPreconditions();
    if (!ok) throw new Error('Preconditions changed; try again.');
    return runAction();
  }
  return <button disabled={disabled} onClick={onClick}>Run</button>;
}
```

4) Respect user/environment preferences in UI behavior
- Where browser/user preferences exist (e.g., `prefers-reduced-motion`), use them to choose behavior by default.
- Allow explicit props to override, but don’t ignore preferences by hardcoding behavior.