---
title: Consistent Config Resolution
description: When configuration affects behavior (URLs, remotes, session/bootstrap
  identifiers, feature toggles), resolve it once from a single source of truth, reuse
  the exact resolved value everywhere, and avoid side-effect mutations. Also ensure
  env/flag precedence is deterministic and tests isolate configuration.
repository: cline/cline#v16
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70882
---

When configuration affects behavior (URLs, remotes, session/bootstrap identifiers, feature toggles), resolve it once from a single source of truth, reuse the exact resolved value everywhere, and avoid side-effect mutations. Also ensure env/flag precedence is deterministic and tests isolate configuration.

Guidelines:
1) Single source of truth
- Prefer shared helpers for mapping provider/backend/base URLs, env-key detection, and remote selection.
- Don’t duplicate “choose X” logic in multiple places (it’s easy for manifest/UI to diverge from push/runtime targets).

2) Resolve once, not per refresh
- Compute environment-dependent values at startup (or at the same lifecycle boundary as the rest of the configuration), then pass them through.

3) No observer-side mutation of bootstrap config
- If you attach telemetry/hooks or otherwise “observe” start state, do not rewrite fields that upstream logic uses to decide behavior (e.g., sessionId affecting restart vs new).
- Clone/extend only the fields you own; otherwise return the original config shape.

4) Deterministic precedence for flags vs env
- For negatable flags (e.g., `--no-*`), don’t rely on raw option values; use option/source metadata so defaults don’t clobber env fallbacks.

5) Test isolation for configuration
- Tests should clear or control relevant env vars (e.g., proxy vars) so behavior is stable and not dependent on the developer/CI environment.

Example patterns:

- Avoid bootstrapping mutation:
```ts
function configure(originalConfig: CoreStartConfig, hooks: Hook[]) {
  // GOOD: don’t rewrite sessionId (or other bootstrap fields)
  return { ...originalConfig, hooks };

  // BAD: changing fields that core interprets can flip behavior
  // return { ...originalConfig, sessionId: originalConfig.sessionId ?? mintedId, hooks };
}
```

- Deterministic precedence for negatable flags:
```ts
const mouse =
  (authCmd.getOptionValueSource("mouse") === "cli" ? authCmd.opts().mouse : undefined) ??
  (program.getOptionValueSource("mouse") === "cli" ? program.opts().mouse : undefined);
```

Apply this standard to URL/baseUrl/remote selection, telemetry/bootstrap wiring, and all env/flag handling paths to prevent subtle environment mismatches and nondeterministic behavior.