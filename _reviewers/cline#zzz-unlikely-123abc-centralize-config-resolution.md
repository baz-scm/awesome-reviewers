---
title: Centralize config resolution
description: When a setting can come from multiple sources (saved provider settings,
  environment variables, CLI flags, startup context), resolve it through a single
  shared function with an explicit, documented precedence order, and reuse that function
  everywhere the value is needed instead of letting each call site re-implement its
  own logic. Divergent resolution rules...
repository: cline/cline#zzz-unlikely-123abc
label: Configurations
language: TypeScript
comments_count: 11
repository_stars: 71035
---

When a setting can come from multiple sources (saved provider settings, environment variables, CLI flags, startup context), resolve it through a single shared function with an explicit, documented precedence order, and reuse that function everywhere the value is needed instead of letting each call site re-implement its own logic. Divergent resolution rules caused real bugs: account links opened the wrong environment because the link builder used `appBaseUrl` while API calls used the provider `baseUrl` override (fixed by introducing one `resolveClineAppBaseUrl(apiBaseUrl)` used by both the privacy link and the dashboard link); two git-remote lookups used different fallback order and could point at different repos; a `--no-mouse` flag was wired into a test-only parser while the real CLI path kept reading raw env vars.

Apply these rules:
- One canonical resolver per concept (API key, base URL, remote URL, env-key detection) — do not reintroduce parallel/legacy fields or ad-hoc duplicate logic (e.g., rejecting a second `lmStudioApiKey` field once a single `ProviderSettings.apiKey` store existed).
- When a value is fixed for the life of a process (app base URL, host name), resolve it once at startup and store it in context/registry rather than re-deriving it from live settings on every call.
- When multiple sources can set the same option (CLI flag, env var, caller-supplied override, derived default), define and test the precedence explicitly — e.g. check `getOptionValueSource("x") === "cli"` rather than trusting a default-populated option value, and let an explicitly passed option win over a computed default (`allowBindFallback` caller value wins over `!hasExplicitEndpoint`).
- Isolate environment-dependent config in tests/builds (set `CLINE_DIR`, `CLINE_HUB_DISCOVERY_PATH`, etc. inside a temp dir) so test runs never read or mutate a developer's real configuration.
- Verify the full resolution path end-to-end (all flag/env combinations, all call sites) rather than only the entry point, since the real runtime path may differ from a test-only parser.

Example precedence helper:
```ts
const useMouse =
  input.mouse !== undefined
    ? input.mouse
    : process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0";
```