---
title: Centralize environment URL building
description: When configuration (env base URLs, attribution, feature flags) affects
  UI behavior, centralize its usage and avoid leaking identity-derived values through
  shared contexts.
repository: cline/cline#v23
label: Configurations
language: TSX
comments_count: 3
repository_stars: 70889
---

When configuration (env base URLs, attribution, feature flags) affects UI behavior, centralize its usage and avoid leaking identity-derived values through shared contexts.

Apply these rules:
1) Scope context correctly
- Keep shared providers limited to stable environment configuration (e.g., `clineAppBaseUrl`).
- Derive account/user-dependent links inside the view/component that already has (or fetches) the needed user, rather than duplicating it into context for link duplication.

2) Use one URL/link builder per environment
- Generate all environment-sensitive links through a single builder that consumes the resolved env base URL + any required attribution.
- Do not hardcode production host constants in UI routes if the same links should honor the configured environment.

3) Provide deterministic fallbacks
- If required config is missing/unresolved, produce a safe default (e.g., fall back to production) so buttons/links don’t become `undefined` and disappear.

4) Gate UX based on config/state, not just feature flags
- For feature-flagged actions, hide/disable the command up front when the necessary state isn’t available (e.g., no GitHub connection), while still performing runtime checks (dirty state, validation) when the action is executed.

Example pattern (URLs)
```ts
// env-based URL builder (single source of truth)
const PROD_BASE = "https://app.cline.bot";

export function buildAppUrl(path: string, base?: string) {
  const resolvedBase = base ?? PROD_BASE; // fallback to keep UI deterministic
  return `${resolvedBase}${path}`;
}

// In AccountView-like component:
function AccountView() {
  const { clineAppBaseUrl } = useAccount();
  const dashboardUrl = buildAppUrl("/dashboard", clineAppBaseUrl);
  // All buttons use dashboardUrl/other buildAppUrl(...) outputs
}
```

This standard prevents inconsistent environments, reduces fragile context plumbing, and improves self-hosted/proxy reliability by ensuring configuration changes are reflected uniformly across the UI.