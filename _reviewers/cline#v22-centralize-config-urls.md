---
title: Centralize config URLs
description: For any UI that depends on environment-specific configuration (app base
  URL, attribution, proxies/self-hosting), use a single source of truth to build links
  and avoid leaking account-derived identity into global/shared configuration.
repository: cline/cline#v22
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70886
---

For any UI that depends on environment-specific configuration (app base URL, attribution, proxies/self-hosting), use a single source of truth to build links and avoid leaking account-derived identity into global/shared configuration.

Apply this standard:
- Centralize all env-specific URL construction in one builder (based on the resolved config/base URL) and route every related account/app link through it so users don’t get mixed environments or production fallbacks.
- Keep identity-derived links (e.g., privacy settings URLs that depend on the fetched user) derived inside the owning component/view; don’t add those derived values to shared contexts solely to support duplicated UI.
- Expose only true environment configuration in shared context/providers (e.g., `clineAppBaseUrl`), and pass account/user data locally.
- When a feature flag enables an action, gate visibility/availability using required preconditions derived from config/state (not only the flag), while still validating critical conditions at runtime.

Example (pattern):
```ts
// env/config context: only env config
type AppConfig = { clineAppBaseUrl?: string };

function buildAppUrl(appBaseUrl: string | undefined, path: string) {
  if (!appBaseUrl) return undefined;
  return new URL(path, appBaseUrl).toString();
}

function AccountView() {
  const { clineAppBaseUrl } = useAppConfig();
  const user = useUser(); // local fetch

  const privacyUrl = buildAppUrl(
    clineAppBaseUrl,
    `/privacy?user=${encodeURIComponent(user.id)}`
  );

  return privacyUrl ? <a href={privacyUrl}>Privacy settings</a> : null;
}
```