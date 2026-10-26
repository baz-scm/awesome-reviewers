---
title: Configuration resolution consistency
description: When code derives behavior from configuration (env vars, provider settings,
  feature flags, CLI args), it must (1) use one canonical resolution path, (2) resolve
  at the appropriate time (often startup), (3) apply deterministic precedence, and
  (4) avoid mutating semantic “bootstrap truth” that controls core behavior.
repository: cline/cline#v19
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70885
---

When code derives behavior from configuration (env vars, provider settings, feature flags, CLI args), it must (1) use one canonical resolution path, (2) resolve at the appropriate time (often startup), (3) apply deterministic precedence, and (4) avoid mutating semantic “bootstrap truth” that controls core behavior.

**Rules**
1. **Resolve once using shared helpers**: Compute derived config (e.g., backend app base URL, default model id, API-key presence) once from the canonical inputs, then reuse the exact value for all downstream uses (service calls, URLs/links, webviews).
2. **Unify selection logic**: If multiple parts choose “the same” thing (remote/repo URL, base URL, default model), they must follow the same rule set to prevent UI/reporting mismatch vs actual targets.
3. **Deterministic precedence for env vs CLI**: For CLI flags (especially negatable ones), don’t rely on raw option values; use the option’s value source to decide whether to honor CLI or fall back to env.
4. **No observer mutation of bootstrap fields**: Telemetry/observers may attach hooks/side effects, but they must not rewrite fields that core interprets as semantic signals (e.g., `sessionId`).

**Example (env/CLI precedence for negatable flags)**
```ts
const mouse =
  cliMouseProvided ? authCmd.opts().mouse : undefined;
const resolved =
  mouse ?? (programMouseProvided ? program.opts().mouse : undefined) ??
  (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```

**Example (don’t mutate bootstrap truth)**
```ts
// Incorrect: mutating/overwriting core semantic inputs
// this.config.sessionId = mintedId

// Correct: keep original semantic inputs; only add hooks
return { ...originalConfig, hooks };
```

Adopting this avoids mismatched environments/targets, prevents surprising behavior from flag/env fallbacks, and keeps configuration layers safe and predictable.