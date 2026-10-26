---
title: Centralized Config-Aware Links
description: 'When configuration and environment determine what an action/link should
  do, implement it in a single, consistent way:


  - Gate UI availability using real prerequisites (workspace manifest, connection
  state, resolved environment base URL) rather than feature flags alone. If you can’t
  validate everything at render time, hide/disable the action until...'
repository: cline/cline#v15
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70877
---

When configuration and environment determine what an action/link should do, implement it in a single, consistent way:

- Gate UI availability using real prerequisites (workspace manifest, connection state, resolved environment base URL) rather than feature flags alone. If you can’t validate everything at render time, hide/disable the action until prerequisites are known, and still re-validate the critical conditions at runtime.
- Keep environment/config values separate from account identity. Expose only true configuration in shared context; derive account-specific links inside the view that owns the fetched user/account state.
- Centralize environment-aware URL generation (base URL resolution + client attribution) so all account/settings links use the same builder and behavior (including fallback strategy when the base URL can’t be resolved).

Example pattern:
```ts
// envUrlBuilder.ts
export function buildAppUrl(path: string, { fallback }: { fallback: string }) {
  const base = process.env.APP_BASE_URL; // or resolved from config
  const resolved = base ? `${base.replace(/\/$/, '')}/${path.replace(/^\//, '')}` : undefined;
  return resolved ?? fallback;
}

// account-view.tsx
const dashboardUrl = buildAppUrl('dashboard', { fallback: 'https://app.cline.bot/dashboard' });

// action gating
const canShow = hasGitRemote && githubConnected && appBaseUrlResolved;
// still validate before execution
async function runAction() {
  await ensureCleanWorkingTree(); // runtime check
  await ensureRemoteAccessible(); // runtime check
}
```
This prevents users from discovering missing prerequisites only after clicking, avoids link inconsistencies across environments (self-hosted/proxy), and reduces state synchronization complexity by keeping config separate from account-derived data.