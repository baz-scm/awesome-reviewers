---
title: Centralize Environment URL Building
description: When building user-facing links/actions that vary by environment (cloud
  vs self-hosted, proxy setups, etc.), treat the resolved “app base URL” (and other
  environment-derived config) as a single source of truth and propagate it consistently.
repository: cline/cline#v11
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70871
---

When building user-facing links/actions that vary by environment (cloud vs self-hosted, proxy setups, etc.), treat the resolved “app base URL” (and other environment-derived config) as a single source of truth and propagate it consistently.

Apply these rules:
1) Resolve environment configuration centrally (don’t rely on the webview to “know” env).
- If the UI can’t determine `CLINE_ENVIRONMENT`, have a trusted component (e.g., sidecar) return the resolved app base URL (or equivalent) and hide env-dependent links when it’s unavailable.

2) Use one URL builder for all environment-sensitive links.
- Avoid hardcoded production endpoints for items shown in the same environment-dependent view. Instead, generate every such link through the same builder, so users don’t land in mixed environments.

3) Keep environment config separate from account identity.
- Shared context should contain environment-only values (e.g., `clineAppBaseUrl`) but not user-dependent artifacts needed only to render a duplicated link. Derive privacy/user links inside the view that fetches the user.

4) Gate actions/commands based on resolved config/state early, but still validate at runtime.
- Don’t show an action just because a feature flag is enabled; also check capability/connection state (from workspace manifest and/or cloud-reported status). Still perform the authoritative runtime checks (e.g., dirty state / remote listing) when the action runs.

Example pattern (self-contained):
```ts
// env-only shared config (e.g., from sidecar/command)
type EnvConfig = { appBaseUrl?: string };

function buildAppUrl(appBaseUrl: string, path: string) {
  return `${appBaseUrl.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
}

// View-specific derived link (identity-dependent)
function buildPrivacySettingsUrl(appBaseUrl: string | undefined, userPrivacyPath?: string) {
  if (!appBaseUrl || !userPrivacyPath) return undefined;
  return buildAppUrl(appBaseUrl, userPrivacyPath);
}

// UI gating: hide when unresolved; still validate on run
const privacyUrl = buildPrivacySettingsUrl(env.appBaseUrl, user?.dataPrivacyPath);
const canRunAction = featureFlag && userGitConnected && !isCloudExpired;

return (
  <>
    {privacyUrl ? <a href={privacyUrl}>Privacy settings</a> : null}
    <button disabled={!canRunAction} onClick={runWithRuntimeValidation}>Open dashboard</button>
  </>
);
```
