---
title: Honor config consistently
description: 'Treat configuration (feature flags, env base URLs, and user preference
  settings) as a first-class input to both UI and behavior.


  Apply these rules:

  1) Gate capabilities early: If a command/link depends on external state (e.g., GitHub
  connection + feature flag), hide/disable it in the UI before execution using known
  workspace/session data; still perform...'
repository: cline/cline?x=1
label: Configurations
language: TSX
comments_count: 5
repository_stars: 70861
---

Treat configuration (feature flags, env base URLs, and user preference settings) as a first-class input to both UI and behavior.

Apply these rules:
1) Gate capabilities early: If a command/link depends on external state (e.g., GitHub connection + feature flag), hide/disable it in the UI before execution using known workspace/session data; still perform required safety checks at runtime (e.g., dirty state/`ls-remote`).
2) Centralize environment-dependent URLs: Use a single builder that takes the resolved environment base URL and applies consistently to all links in a view. Avoid leaving links undefined—either provide a safe fallback (commonly production) or hide the specific action with the reason.
3) Keep identity vs environment separate: Don’t publish account-identity-derived values into shared configuration context if the view can derive them from its own fetched user data; keep environment config (like `clineAppBaseUrl`) distinct from account refresh/state.
4) Resolve preference-driven behavior from the source of truth: For user/system preferences (e.g., `prefers-reduced-motion`), pick behavior based on the media query by default, but allow an explicit prop override.

Example (environment URL builder + safe fallback):
```ts
function buildAppUrl(appBaseUrl: string | undefined, path: string) {
  const base = appBaseUrl ?? "https://app.cline.bot"; // fallback for missing env
  return new URL(path, base).toString();
}

// Use for every environment-dependent account link
const dashboardUrl = buildAppUrl(clineAppBaseUrl, "/dashboard");
const privacyUrl = buildAppUrl(clineAppBaseUrl, "/privacy");
```

Testing guidance: add unit/component tests for both branches of config-driven behavior (e.g., with/without resolved env URL; reduced-motion vs normal motion; enabled vs disabled based on prerequisites).