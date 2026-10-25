---
title: Env-aware actions and links
description: For configuration-dependent behavior (feature flags, environment base
  URLs, self-hosted/proxy setups), ensure UI availability and navigation are determined
  consistently from config/state *before* the user triggers the action, and that environment-specific
  URLs are generated via a single, centralized mechanism.
repository: cline/CLINE
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70839
---

For configuration-dependent behavior (feature flags, environment base URLs, self-hosted/proxy setups), ensure UI availability and navigation are determined consistently from config/state *before* the user triggers the action, and that environment-specific URLs are generated via a single, centralized mechanism.

**Apply this checklist**
- **Gate up front:** When an action depends on external/config state (e.g., GitHub connection), show/enable it only when that state is known, not just when a feature flag is true. Still keep **runtime safety checks** (e.g., dirty-state checks).
- **Centralize URL generation:** Use one URL builder that applies the resolved environment base + attribution consistently across all account-related links (dashboard, privacy, usage, credits, org links). Avoid hardcoded production constants scattered across components.
- **Handle missing env resolution safely:** If the environment base URL is unresolved, don’t leave links undefined and hide buttons silently—use a **fallback** (commonly production) so self-hosted/proxy users don’t regress.
- **Separate config from identity plumbing:** Keep **environment configuration** (e.g., app base URL) separate from **account identity/privacy** data. Derive account/privacy links in the account view (or a dedicated helper) instead of duplicating account-derived values into global context to support duplicate UI elsewhere.

**Example pattern (centralized builder + safe fallback)**
```ts
function buildAppUrl(path: string, base?: string) {
  const resolvedBase = base ?? "https://app.cline.bot"; // fallback
  return `${resolvedBase}${path}`;
}

// Usage: all account links share the same builder
const dashboardUrl = buildAppUrl(`/dashboard`, clineAppBaseUrl);
const privacyUrl = buildAppUrl(`/privacy`, clineAppBaseUrl);
```

**Outcome:** fewer environment mismatches, no duplicated account/privacy wiring, and actions/links behave predictably across cloud, local, proxy, and self-hosted configurations.