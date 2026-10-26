---
title: Consistent config-based links
description: When code depends on environment/configuration (base URLs, feature availability,
  privacy endpoints), make link generation and visibility consistent, early, and centralized.
repository: cline/cline#v18
label: Configurations
language: TSX
comments_count: 5
repository_stars: 70884
---

When code depends on environment/configuration (base URLs, feature availability, privacy endpoints), make link generation and visibility consistent, early, and centralized.

Apply these rules:
1) Resolve environment config once
- Fetch environment/base URL during app startup (or the first successful provider mount).
- Don’t re-fetch it on every account refresh; reconnect should only retry initial resolution if it previously failed.

2) Centralize all environment-specific link building
- Use one URL builder that consumes the resolved base URL and applies attribution consistently.
- Avoid hardcoded production URLs for environment-sensitive links.
- If the resolved base URL is unavailable, ensure the UX falls back predictably (e.g., hide only if truly optional; otherwise fall back to production or a safe default).

3) Keep context focused (separate account identity from environment config)
- Don’t add account-derived privacy URLs or user-dependent actions into global account context solely to duplicate UI.
- Let the Account view derive its privacy/settings links from the user it fetches.
- Only expose environment configuration values that are stable for the app lifetime.

4) Gate actions/commands up front using known state
- Don’t rely on feature flags alone; hide/disable UI until prerequisites are known.
- Still perform critical run-time checks when the action executes (e.g., dirty state / remote existence), since state can change.

Example pattern (URL resolve-once + centralized builder):
```ts
// Provider: resolve env config once
const [appBaseUrl, setAppBaseUrl] = useState<string | undefined>(undefined);
useEffect(() => {
  let cancelled = false;
  (async () => {
    try {
      const url = await desktopClient.invoke<string>("get_cline_app_base_url");
      if (!cancelled) setAppBaseUrl(url);
    } catch {
      // keep undefined; callers can fall back or hide
    }
  })();
  return () => { cancelled = true; };
}, []);

// Central builder: used by every account link
const buildAppUrl = (path: string) => {
  const base = appBaseUrl ?? "https://app.cline.bot"; // fallback policy
  const attribution = "?utm_source=desktop";
  return `${base}${path}${attribution}`;
};

// UI: use builder consistently
const dashboardUrl = buildAppUrl(`/dashboard/${userId}`);
```