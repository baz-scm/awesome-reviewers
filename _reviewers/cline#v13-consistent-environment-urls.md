---
title: Consistent Environment URLs
description: 'Treat environment-specific configuration (e.g., app base URL) as a resolved,
  stable input that is centralized and applied consistently across the UI.

  '
repository: cline/cline#v13
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70874
---

Treat environment-specific configuration (e.g., app base URL) as a resolved, stable input that is centralized and applied consistently across the UI.

Practical rules:
1) Centralize URL generation: create one builder that uses the resolved environment/base URL + attribution, and route all account/dashboard/privacy/open links through it (avoid mixing environment-aware links with hardcoded production URLs).
2) Resolve config once: look up environment configuration once at startup (or first successful lookup) and reuse it across account refreshes/reconnects; retries should only cover initial failures.
3) Separate identity from env config: don’t stuff view-derivable account links (like privacy/settings URLs) into account identity context. Keep identity context for account/user data; keep env configuration in a separate field or dedicated provider.
4) Gate UI actions up front: if a command/CTA requires external state (e.g., GitHub connection), determine availability using cheap known info (manifest/session state or a lightweight status call) before the user runs the action; still validate correctness at runtime (dirty state / `ls-remote`, etc.).

Example pattern (centralized builder + stable resolved base):
```ts
// resolved once on provider mount / first successful lookup
const [appBaseUrl, setAppBaseUrl] = useState<string | undefined>();

useEffect(() => {
  void desktopClient.invoke<string>("get_cline_app_base_url").then(setAppBaseUrl).catch(() => {
    // hide env-dependent links until resolved
  });
}, []);

function buildDashboardUrl(path: string) {
  if (!appBaseUrl) return undefined;
  return `${appBaseUrl}/${path}?attribution=${encodeURIComponent("client")}`;
}

// Use builder for all related account links
const dashboardUrl = buildDashboardUrl("dashboard");
const usageUrl = buildDashboardUrl("usage");
```

Applying this prevents inconsistent environment routing, reduces unnecessary config churn, keeps context boundaries clean, and improves user experience by hiding or gating actions until required config/state is available.