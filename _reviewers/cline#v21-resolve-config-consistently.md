---
title: Resolve config consistently
description: 'Apply configuration-driven logic consistently: resolve environment/user
  configuration once (via centralized builders), use it to gate UI/actions early,
  and provide safe fallbacks when config can’t be resolved.'
repository: cline/cline#v21
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70886
---

Apply configuration-driven logic consistently: resolve environment/user configuration once (via centralized builders), use it to gate UI/actions early, and provide safe fallbacks when config can’t be resolved.

How to apply:
- Centralize builders for environment-specific links (app base URL, attribution, proxies/self-hosted). Avoid mixing hardcoded production URLs with environment-aware ones.
- Gate buttons/commands using the best-known config/state available at render/session start (e.g., manifest git info, connection availability). Still perform authoritative runtime checks (dirty state, remote probing) when the action actually runs.
- If resolved config is unavailable, define an explicit fallback strategy (e.g., production) so links don’t become undefined/hidden unexpectedly.
- For preference-driven behavior (e.g., motion settings), resolve from the user/environment configuration unless explicitly overridden by props, and cover both paths with tests.

Example pattern (URL/config builder + fallback):
```ts
function buildDashboardUrl({ appBaseUrl, attribution, fallbackBaseUrl }) {
  const base = appBaseUrl ?? fallbackBaseUrl; // explicit fallback
  if (!base) return null;
  const url = new URL('/dashboard', base);
  url.searchParams.set('client', attribution);
  return url.toString();
}

// usage: all links in the account view call the same builder
const dashboardUrl = buildDashboardUrl({
  appBaseUrl: clineAppBaseUrl,
  attribution: clientAttribution,
  fallbackBaseUrl: 'https://app.cline.bot',
});
```