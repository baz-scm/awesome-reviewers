---
title: Environment-aware UI gating
description: 'When UI behavior depends on configuration/environment or user/system
  preferences, make it consistent, early, and locally derived.


  Apply:

  1) Centralize env/config URL building and link policies'
repository: cline/cline#v4
label: Configurations
language: TSX
comments_count: 5
repository_stars: 70864
---

When UI behavior depends on configuration/environment or user/system preferences, make it consistent, early, and locally derived.

Apply:
1) Centralize env/config URL building and link policies
- Build account/settings URLs from the resolved base URL (and attribution) in one place.
- Ensure a defined fallback (e.g., production or the last-known base) so links/buttons don’t silently become undefined for proxy/self-hosted setups.

2) Gate capability visibility up front
- Don’t rely on feature flags or “run-time discovery” inside the action path.
- Use available session/workspace/config state to determine whether to show/enable a command/link before the user clicks.
- Still keep run-time validations (e.g., dirty state / server checks) before performing the action.

3) Keep context scoped to true config
- Global/provider context should expose stable environment/config values.
- Avoid publishing account-identity-derived fields (like privacy/user-specific URLs) when the destination view can derive them locally from fetched user data.

4) Respect preference-derived defaults
- If behavior is influenced by user/system preferences (e.g., `prefers-reduced-motion`), use the preference as the default while allowing explicit props to override.
- Add tests covering both preference and override cases.

Example pattern (URL builder + fallback):
```ts
function buildAccountUrl(opts: { baseUrl?: string; path: string }) {
  const base = opts.baseUrl ?? "https://app.cline.bot"; // fallback
  return new URL(opts.path, base).toString();
}

const dashboardUrl = buildAccountUrl({ baseUrl: clineAppBaseUrl, path: "/dashboard" });
```

This prevents mixed-environment navigation, duplicated settings entries, late/hidden command discovery, and preference-ignoring UX regressions.