---
title: Centralize config-derived actions
description: 'Define a single, configuration-aware layer for “what the user can do”
  and “where links go,” and avoid duplicating derived account/config state.


  **Rules**'
repository: cline/cline#v9
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70868
---

Define a single, configuration-aware layer for “what the user can do” and “where links go,” and avoid duplicating derived account/config state.

**Rules**
1) **Centralize env URL generation**
- Create a single URL builder that uses the resolved environment base URL + any required attribution/client parameters for all account-related links.
- If the base URL is not resolved, **fall back** to the intended default (e.g., production) so buttons don’t become hidden/undefined.

2) **Scope privacy/account links to the correct owner**
- Place privacy/data-sharing actions in the **Account** area (not Telemetry/General) to keep UI semantics aligned.
- Don’t add account-derived links/props into unrelated contexts just to support duplicated UI.

3) **Gate feature-flagged actions up front**
- If an action depends on prerequisites (e.g., GitHub connection, workspace git metadata), compute an “enabled/visible” state using cheap session/workspace data (and cloud connection state when available) **before** the user runs the command.
- Still perform critical runtime checks (e.g., dirty state / `ls-remote`) when the action executes.

**Example (env URL builder + fallback)**
```ts
function buildAppUrl(appBaseUrl: string | undefined, path: string) {
  const base = appBaseUrl ?? "https://app.cline.bot"; // fallback default
  return `${base}${path}`; // include attribution/client params as needed
}

// Use the builder for every link in the account view
const dashboardUrl = buildAppUrl(clineAppBaseUrl, "/dashboard");
```

Applying these keeps configuration behavior consistent across environments, prevents hidden/undefined links, and reduces user-facing surprises from feature flags or duplicated account-derived state.