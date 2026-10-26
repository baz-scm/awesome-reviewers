---
title: Centralize Config-Driven Links
description: All environment-specific behavior (URLs, visibility/enabled state for
  configured features) should be derived from a single, resolved configuration source—never
  scattered hardcoded constants or late-discovery gating.
repository: cline/cline#v24
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70891
---

All environment-specific behavior (URLs, visibility/enabled state for configured features) should be derived from a single, resolved configuration source—never scattered hardcoded constants or late-discovery gating.

Apply these rules:
1) Centralize URL generation: create one builder that takes the resolved environment/app base URL and any attribution/client parameters, then use it for every link that depends on environment.
2) Define a fallback policy: if the resolved app base URL is unavailable, don’t leave handlers producing `undefined` and hiding buttons implicitly—either consistently fall back (e.g., to production) or consistently hide/disable with a clear reason.
3) Gate up front, validate at runtime: enable/offer actions using feature flags + workspace/session state + any known cloud/config availability before the user runs the command; still perform required runtime checks (e.g., dirty state, `ls-remote`).
4) Separate config from identity in context: keep environment configuration (e.g., app base URL) in a dedicated config provider; derive identity-dependent links inside the owning view (e.g., AccountView) rather than syncing user-derived link data through shared account context.

Example (env-aware URL builder + consistent link usage):
```ts
type UrlBuilderDeps = {
  appBaseUrl?: string; // resolved from env
  clientAttribution?: string;
};

function buildAppUrl(path: string, { appBaseUrl, clientAttribution }: UrlBuilderDeps) {
  if (!appBaseUrl) {
    // Fallback policy: either return production explicitly or throw
    // return `https://app.cline.bot${path}`;
    return undefined;
  }
  const url = new URL(path, appBaseUrl);
  if (clientAttribution) url.searchParams.set("attribution", clientAttribution);
  return url.toString();
}

// In AccountView
const dashboardUrl = buildAppUrl("/dashboard", deps);
// Use dashboardUrl consistently across all related account links/buttons.
```

Outcome: users are routed to the correct environment consistently, feature actions appear only when configuration/session state indicates they should, and context synchronization stays clean and low-risk.