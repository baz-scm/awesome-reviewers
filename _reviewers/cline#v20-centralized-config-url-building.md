---
title: Centralized Config URL Building
description: 'Use one source of truth for environment/config-driven URLs and availability,
  and avoid unnecessary global plumbing.


  Apply this in practice:

  - Centralize environment-specific URL construction (app base URL, attribution, query
  params) in a single builder function.'
repository: cline/cline#v20
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70886
---

Use one source of truth for environment/config-driven URLs and availability, and avoid unnecessary global plumbing.

Apply this in practice:
- Centralize environment-specific URL construction (app base URL, attribution, query params) in a single builder function.
- Use that builder for *all* related links in a feature (don’t mix hardcoded production URLs and environment-based URLs in the same view).
- If the resolved environment base URL is unavailable, fall back to a safe default (e.g., production) so UI doesn’t silently disappear. Avoid “undefined => hide” behavior.
- Determine whether a command/button should be shown using cheap, known state/config early (not feature flags alone), but still re-check critical runtime preconditions (e.g., dirty state, remote availability) right before executing.
- Keep shared/global context limited to true environment configuration; compute user-specific link targets inside the owning view that fetches/knows the user.

Example pattern (self-contained):
```ts
type LinkCtx = { appBaseUrl?: string; attribution?: string };

function buildAppUrl(path: string, { appBaseUrl, attribution }: LinkCtx) {
  const base = appBaseUrl ?? 'https://app.cline.bot'; // production fallback
  const url = new URL(path, base);
  if (attribution) url.searchParams.set('attribution', attribution);
  return url.toString();
}

// In a view/component
const { appBaseUrl, attribution } = envConfig;
const dashboardUrl = buildAppUrl('/dashboard', { appBaseUrl, attribution });
```

This prevents inconsistent environments (mixed hardcoded vs resolved URLs), reduces duplicate link logic, and ensures missing config doesn’t degrade UX into hidden actions.
