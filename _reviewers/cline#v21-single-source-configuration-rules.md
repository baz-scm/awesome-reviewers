---
title: Single-source Configuration Rules
description: When configuration drives behavior, ensure there is exactly one shared,
  authoritative interpretation, resolved at the right lifecycle point, with explicit
  precedence—and do not mutate bootstrap/authority config fields.
repository: cline/cline#v21
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70886
---

When configuration drives behavior, ensure there is exactly one shared, authoritative interpretation, resolved at the right lifecycle point, with explicit precedence—and do not mutate bootstrap/authority config fields.

Apply these rules:
- Centralize logic: If the SDK/runtime already defines how to parse/interpret config (frontmatter enablement, provider env-key detection, provider readiness, URL mapping), call the shared helper/contract rather than re-implementing in each UI/app layer.
- Resolve once: Compute environment-specific values (e.g., app base URLs derived from the backend actually contacted) once during startup/config resolution, then pass the resolved value downstream; avoid re-resolving on every account refresh.
- Make precedence explicit: For feature flags and CLI/env combinations, treat “explicitly provided by CLI” differently from “defaulted.” Use option-value-source mechanisms rather than raw negatable option values, so env fallbacks aren’t clobbered.
- Don’t rewrite authority: Layering features (telemetry, onboarding UX, webview actions) should add hooks/side effects, not change semantic bootstrap fields that downstream components use to decide control flow (e.g., sessionId/resume vs restart).

Example (CLI precedence with negatable flags):
```ts
const cliMouse = (authCmd.getOptionValueSource('mouse') === 'cli')
  ? authCmd.opts().mouse
  : undefined;

const mouse = cliMouse ??
  (program.getOptionValueSource('mouse') === 'cli' ? program.opts().mouse : undefined) ??
  (process.env.CLINE_NO_MOUSE !== '1' && process.env.CLINE_MOUSE !== '0');
```

Example (URL mapping resolved once from backend):
```ts
const apiBaseUrl = resolveAccountApiBaseUrl(/* provider + overrides */);
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // maps backend->environment
const privacyUrl = getClinePrivacySettingsUrl(user.dataPrivacyPath, appBaseUrl, 'cli');
```

If you find yourself adding a second “flag” or copying parsing/decision logic, or mutating core config fields to “make it work,” it’s a sign the configuration rules need to be unified, resolved once, and layered safely.