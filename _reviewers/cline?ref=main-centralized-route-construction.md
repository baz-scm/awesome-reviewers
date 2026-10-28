---
title: Centralized route construction
description: Avoid hardcoding or duplicating URL/path strings across components; instead,
  centralize route construction in a shared helper (e.g., a `getClineUris` utility)
  that mirrors the app's routing configuration, including any `next.config.ts` redirects.
  This keeps links consistent across surfaces (web, desktop, CLI) and ensures that
  when a route changes, it only...
repository: cline/cline?ref=main
label: Next
language: TSX
comments_count: 2
repository_stars: 70980
---

Avoid hardcoding or duplicating URL/path strings across components; instead, centralize route construction in a shared helper (e.g., a `getClineUris` utility) that mirrors the app's routing configuration, including any `next.config.ts` redirects. This keeps links consistent across surfaces (web, desktop, CLI) and ensures that when a route changes, it only needs to be updated in one place rather than hunted down across every component that links to it.

```ts
// Good: single source of truth, aligned with next.config.ts redirects
const dashboardUrl = buyCreditsUrl ?? getClineUris(appBaseUrl, "credits", orgId ? "organization" : "account")

// Avoid: ad-hoc path construction duplicated per component
const dashboardUrl = buyCreditsUrl ?? (orgId ? DEFAULT_BUY_CREDITS_URL.ORG : DEFAULT_BUY_CREDITS_URL.USER)
```

Additionally, any logic that depends on browser/platform-only APIs (e.g., `window`, Tauri availability, persisted layout state) must be initialized inside `useEffect` rather than during render, so it respects SSR/hydration boundaries and only runs once the client environment is available. Combine this with sane bounds-checking (e.g., clamping restored sizes against `window.innerHeight`, using `ResizeObserver` to refit on resize) so client-only UI state stays consistent after rehydration and across viewport changes.