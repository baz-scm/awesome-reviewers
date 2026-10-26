---
title: Configuration precedence rules
description: 'When multiple configuration inputs can influence behavior (env vars,
  saved provider settings, CLI flags/options, derived defaults, or observer-added
  hooks), make resolution explicit, consistent, and testable:'
repository: cline/cline#v17
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70883
---

When multiple configuration inputs can influence behavior (env vars, saved provider settings, CLI flags/options, derived defaults, or observer-added hooks), make resolution explicit, consistent, and testable:

- Use the same shared resolution helpers/parsers across components (don’t duplicate enablement/url-mapping logic in UI vs SDK/runtime).
- Resolve environment/app/provider URLs once during startup from the already-resolved configuration, and reuse the resolved value (don’t re-read provider settings on each account refresh).
- Define precedence and implement it mechanically. A safe default is:
  1) caller-supplied explicit arguments/options
  2) CLI flag values *only when the framework indicates the value came from CLI* (not framework defaults)
  3) environment variables
  4) persisted settings
  5) derived defaults
- Prevent silent override: if a higher-precedence config is present (e.g., user-pasted API key), ensure lower-precedence data (e.g., leftover auth tokens) cannot win.
- Avoid semantic config mutation: helper/observer code should add hooks/telemetry without rewriting bootstrap truth fields that change core behavior (e.g., sessionId).

Example pattern (precedence + “CLI value source”):

```ts
function resolveSetting(opts: {
  flagValue?: string | boolean;
  flagValueSource?: "cli" | "default" | "env";
}, env: NodeJS.ProcessEnv) {
  // Only trust the flag when it truly came from CLI.
  const fromCli = opts.flagValueSource === "cli" ? opts.flagValue : undefined;

  return (
    fromCli ??
    (env.MY_SETTING?.trim() ? env.MY_SETTING : undefined) ??
    "derived-default"
  );
}
```

Applying this standard prevents mismatched environments/URLs, negatable-flag/env clobbering, leftover auth/token priority bugs, and side-effectful config changes that alter runtime semantics.