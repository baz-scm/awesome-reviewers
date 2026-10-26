---
title: Resolve Once Consistently
description: When config affects behavior or derived links/URLs, resolve it once from
  the authoritative configuration source, then propagate the resolved value—avoid
  recomputing from different inputs in different layers.
repository: cline/cline#v28
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70892
---

When config affects behavior or derived links/URLs, resolve it once from the authoritative configuration source, then propagate the resolved value—avoid recomputing from different inputs in different layers.

Apply these rules:
- **Resolve at the right lifecycle boundary**: compute once at startup (or once per command execution) and reuse across refreshes.
- **Use shared helpers for derived values**: if you have both a backend base URL and a UI/app base URL, derive all links from the same resolved backend input via a shared resolver/helper; hide actions when the mapping is undefined.
- **Centralize “configured readiness” logic**: determine whether a provider is configured using shared provider metadata/contract and env-key helpers (so exclusions and provider-specific requirements match everywhere). Don’t duplicate readiness flags in session/UI payloads.
- **Make precedence explicit (CLI vs env)**: for negatable flags, don’t rely on the raw default value—detect whether the option came from the CLI before overriding env fallbacks.

Example patterns:
```ts
// 1) Resolve backend once, then derive all related links from it.
const apiBaseUrl = resolveBackendBaseUrlFromConfig();
const appBaseUrl = resolveAppBaseUrlFromBackend(apiBaseUrl); // shared helper
const privacySettingsUrl = appBaseUrl
  ? getPrivacySettingsUrl({ apiBaseUrl, appBaseUrl, surface: "cli" })
  : undefined;

// 2) Env readiness via shared helper (no duplicated env-var lists).
const hasKey = isProviderApiKeyEnv(providerId, process.env); // shared

// 3) CLI negatable precedence: use option-source, not raw defaults.
const useMouse = authCmd.getOptionValueSource("mouse") === "cli"
  ? authCmd.opts().mouse
  : process.env.CLINE_MOUSE !== "0" && process.env.CLINE_NO_MOUSE !== "1";
```