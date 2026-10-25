---
title: Config-aware gating and links
description: 'Ensure UI and navigation that depends on environment config or feature
  flags are consistent, preflighted, and deterministic:


  - Centralize environment-specific link construction (use one URL builder so attribution
  and resolved base URLs apply to every button/link in the same view).'
repository: ClInE/cLiNe
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70838
---

Ensure UI and navigation that depends on environment config or feature flags are consistent, preflighted, and deterministic:

- Centralize environment-specific link construction (use one URL builder so attribution and resolved base URLs apply to every button/link in the same view).
- Keep env configuration separate from identity/account-derived state: don’t place account-specific or derived links into app-wide account context when the target view can compute them from fetched user data.
- Gate “available” actions on more than the feature flag: use cheap preflight data available at render/session start to decide whether to show/enable the command; still perform authoritative runtime checks (e.g., dirty state / remote probing) after the user runs it.
- When environment config can’t be resolved, provide a defined fallback (e.g., production) rather than leaving links undefined or hiding UI silently.

Example (centralized builder + fallback):
```ts
type Env = { appBaseUrl?: string };
const defaultBaseUrl = "https://app.cline.bot"; // or production constant

function buildDashboardUrl(env: Env, path: string) {
  const base = env.appBaseUrl ?? defaultBaseUrl;
  const attribution = "?client=desktop"; // example of shared attribution
  return `${base}${path}${attribution}`;
}

// In a view: all buttons use the same builder
const dashboardUrl = buildDashboardUrl(env, "/dashboard");
```

Example (preflight gating with runtime validation preserved):
```ts
const canOffer = featureFlagEnabled && hasGitRemote && hasGitBranch; // cheap session data

<button disabled={!canOffer} onClick={() => {
  // runtime checks still required
  if (isDirty || !lsRemoteOk) return showError();
  runCloudHandoff();
}}>
  Open cloud handoff
</button>
```