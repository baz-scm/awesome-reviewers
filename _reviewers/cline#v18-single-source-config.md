---
title: Single Source Config
description: 'When configuration affects externally visible decisions (URLs, remotes,
  provider readiness, telemetry/session semantics), follow these rules:


  1) Resolve once at the correct lifecycle boundary'
repository: cline/cline#v18
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 70884
---

When configuration affects externally visible decisions (URLs, remotes, provider readiness, telemetry/session semantics), follow these rules:

1) Resolve once at the correct lifecycle boundary
- Compute derived config values (e.g., app base URLs, provider-backed URLs, chosen remote) once during startup or during the single configuration-resolution step.
- Don’t re-resolve on subsequent refresh/account changes unless the feature explicitly supports it.

2) Use one source of truth (shared helpers/contracts)
- Avoid duplicating config flags that represent the same concept across layers (e.g., “providerConfigured” type booleans in multiple places).
- Build links/behavior from the same resolved backend/provider mapping used for the actual runtime action.

3) Make precedence explicit (flag vs env)
- For CLI options, explicitly implement precedence using the option value source; don’t rely on raw option values when the CLI library applies defaults (notably negatable flags like `--no-*`).

4) Never mutate semantic bootstrap truth for other components
- If you’re attaching telemetry/observers, pass through the original bootstrap configuration untouched.
- Don’t rewrite fields that downstream components treat as semantic signals (e.g., `sessionId` meaning “resume vs new”). Attach behavior via hooks/wrappers instead.

Example (explicit CLI precedence for negatable flags):
```ts
const useMouse =
  authCmd.getOptionValueSource("mouse") === "cli"
    ? authCmd.opts().mouse // only trust the value when it came from CLI
    : process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0";
```

Example (don’t mutate semantic config passed to core):
```ts
// BAD: changes bootstrap meaning for core by rewriting semantic fields.
// good: attach telemetry via hooks, without altering core's session semantics.
const original = inputWithRemoteConfig.config;
const coreConfig = { ...original, telemetry: attachTelemetry(original.telemetry), extraTools };
return core.start(coreConfig); // keep original semantic fields meaningfully unchanged
```

Adopting this prevents environment/provider mismatches, config drift between UI/webview and runtime, hidden precedence bugs, and subtle state/telemetry regressions.