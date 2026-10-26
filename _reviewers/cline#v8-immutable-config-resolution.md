---
title: Immutable Config Resolution
description: Ensure configuration derived from environment/config/overrides is resolved
  once from the authoritative source, passed explicitly, and treated as immutable
  input to downstream behavior.
repository: cline/cline#v8
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70867
---

Ensure configuration derived from environment/config/overrides is resolved once from the authoritative source, passed explicitly, and treated as immutable input to downstream behavior.

Do:
- Unify duplicate rules by importing/using shared resolvers/parsers (don’t maintain local “copies” of SDK/runtime enablement, provider-key rules, URL selection rules).
- Resolve override-dependent values once at startup (or the relevant lifecycle point) and reuse the resolved result—avoid per-refresh recomputation that can diverge.
- Make override precedence explicit for CLI flags vs env (especially negatable flags). Use the option-value source to distinguish “user provided” vs “defaulted.”
- Never mutate config objects in a way that changes downstream bootstrap semantics. If you need to attach behavior (telemetry/hooks), return new structures or keep semantic fields unchanged.
- For tests/smoke runs, isolate by setting config/discovery paths to temp dirs so the code can’t read/write real user state.

Example (immutability + explicit precedence):
```ts
// Precedence: use value source rather than raw defaulted value
const mouse = (authCmd.getOptionValueSource("mouse") === "cli")
  ? authCmd.opts().mouse
  : undefined;

// Immutability: don’t rewrite semantic fields the downstream core uses
function configureForTelemetry(input: { config: CoreConfig; hooks: Hooks }) {
  const base = input.config; // keep as-is
  const telemetryConfig: CoreConfig = {
    ...base,
    // only add telemetry-related config; do NOT set/alter sessionId semantics
  };
  return { ...input, config: telemetryConfig };
}
```

Expected outcome: consistent behavior across CLI/env/providers/environments, reduced config drift, and no accidental semantic side effects from helper code.