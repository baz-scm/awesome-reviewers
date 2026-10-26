---
title: Centralize environment config
description: 'Environment-dependent configuration (base URLs, feature endpoints, privacy/dashboard
  links, etc.) must be resolved from a single authoritative source and reused everywhere,
  instead of being hardcoded or re-derived in multiple places. '
repository: cline/cline
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70886
---

Environment-dependent configuration (base URLs, feature endpoints, privacy/dashboard links, etc.) must be resolved from a single authoritative source and reused everywhere, instead of being hardcoded or re-derived in multiple places. 

- Expose environment-specific values (e.g. app base URL) through one backend/sidecar API rather than guessing from client-side env vars that may not be available to the UI layer.
- Build a single shared helper that all consumers call to construct derived URLs/settings (e.g. `buildClineUrl(path)`), so every link—dashboard, usage, credits, privacy settings, onboarding, etc.—consistently honors the configured environment (production, proxy, self-hosted). Replace any hardcoded production constants with calls to this helper; if the environment can't be resolved, hide the affected UI rather than silently falling back to production.
- Resolve this configuration once at startup/initial connection and cache it for the app's lifetime. Only retry the lookup on reconnect if the initial attempt failed—avoid re-fetching on every unrelated refresh (e.g. account refresh), since the backend/environment doesn't change during a session.
- Avoid duplicating a configuration-driven UI element (e.g. a privacy-settings link) across multiple settings sections. Keep each setting's control/action in the one view that owns it, and remove duplicate entries and the extra dependencies they introduce.

Example pattern:
```ts
// single source of truth, resolved once at startup
const appBaseUrl = await desktopClient.invoke<string>("get_cline_app_base_url");

// single builder used by every consumer
function buildClineUrl(path: string): string | undefined {
  return appBaseUrl ? `${appBaseUrl}${path}` : undefined; // hide link if unresolved
}

const dashboardUrl = buildClineUrl("/dashboard");
const privacySettingsUrl = buildClineUrl(user?.dataPrivacyPath ?? "/privacy");
```
This keeps all environment-aware links consistent, avoids drift between hardcoded and dynamic URLs, and prevents unnecessary network calls or UI duplication.