---
title: Centralize environment config resolution
description: Environment-dependent settings (e.g., app base URLs, privacy/dashboard
  links) must be resolved from a single authoritative source and exposed through one
  shared accessor, not hardcoded or re-derived independently in multiple components.
  Since a UI client (webview, frontend) often cannot determine its own runtime environment,
  have the backend/sidecar expose...
repository: cline/cline?foo=bar
label: Configurations
language: TSX
comments_count: 5
repository_stars: 71082
---

Environment-dependent settings (e.g., app base URLs, privacy/dashboard links) must be resolved from a single authoritative source and exposed through one shared accessor, not hardcoded or re-derived independently in multiple components. Since a UI client (webview, frontend) often cannot determine its own runtime environment, have the backend/sidecar expose it via a dedicated command/API, fetch it once at startup (retrying on reconnect only if the initial lookup failed), and cache it for the app's lifetime—avoid re-fetching on every refresh/reconnect when the backend/environment is not expected to change at runtime. All consumers (buttons, links, feature sections) should go through a single builder/helper function that applies this resolved value, rather than scattering hardcoded production URLs or duplicating the same config across unrelated settings sections. This ensures consistent environment behavior (including staging, proxy, and self-hosted setups) everywhere, prevents drift between duplicated UI entries, and makes the one true source easy to test and reason about.

Example pattern:
```ts
// Centralized resolution, fetched once at startup
async function loadAppBaseUrl() {
  try {
    setClineAppBaseUrl(await desktopClient.invoke<string>("get_cline_app_base_url"));
  } catch {
    // retry only on reconnect if still unresolved
  }
}

// Single builder used by every consumer
function buildDashboardUrl(appBaseUrl: string | undefined, path: string) {
  return appBaseUrl ? `${appBaseUrl}${path}` : undefined;
}

// Usage: all links/buttons derive from the same builder instead of hardcoded URLs
const privacySettingsUrl = buildDashboardUrl(clineAppBaseUrl, "/privacy-settings");
const usageUrl = buildDashboardUrl(clineAppBaseUrl, "/usage");
```