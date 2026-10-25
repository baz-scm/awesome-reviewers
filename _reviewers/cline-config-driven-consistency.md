---
title: Config-driven consistency
description: 'When code behavior or links depend on environment variables, feature
  flags, or user preferences, follow these rules:


  1) Centralize env-aware URL building'
repository: CLINE/cline
label: Configurations
language: TSX
comments_count: 5
repository_stars: 70839
---

When code behavior or links depend on environment variables, feature flags, or user preferences, follow these rules:

1) Centralize env-aware URL building
- Use a single URL builder that takes the resolved app base URL (and any attribution/client context) so all account links point to the same environment.
- Avoid hardcoding production URLs for links that should follow the environment.
- Ensure “missing resolved config” doesn’t silently break navigation—provide a sensible fallback instead of hiding buttons/returning undefined.

2) Separate environment config from account identity
- Keep account-derived values (e.g., privacy settings URLs that depend on the fetched user) derived within the view that owns the account fetch.
- Expose only environment configuration (e.g., app base URL) through context if it truly does not change with account refresh.

3) Don’t duplicate account actions across unrelated settings
- Place privacy/data-sharing controls in the Account view (account identity domain), not under telemetry/general settings (feature/diagnostics domain).
- Removing duplicate UI prevents extra cross-context dependencies.

4) Feature flags gate availability, not correctness
- Use feature flags/config to decide whether to show/enable an action, but still validate eligibility at run time (e.g., dirty state checks, remote presence, required external connections).

5) Respect user/environment preferences for UI behavior
- Derive behavior from configuration/preferences (e.g., `prefers-reduced-motion`), and define precedence: an explicit prop/override should win over the preference.

Example (preference resolution with override precedence):
```ts
const prefersReduced = window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches;
const behavior = props.behavior ?? (prefersReduced ? 'auto' : 'smooth');
```

Apply this standard anywhere you wire environment-specific URLs, feature-flagged commands, or preference-sensitive UI behavior.