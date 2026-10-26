---
title: Config Compatibility & Env Safety
description: When configuration behavior changes (new keys, renamed/repurposed toggles,
  UI pickers, feature-gates), ensure user intent is preserved and avoid unsafe process-wide
  environment side effects.
repository: microsoft/VSCode
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 194303
---

When configuration behavior changes (new keys, renamed/repurposed toggles, UI pickers, feature-gates), ensure user intent is preserved and avoid unsafe process-wide environment side effects.

Guidelines:
1) Preserve backward compatibility
- If legacy settings were explicitly set by users, migrate their effective values into the new logic.
- Never silently stop consuming an opt-in key unless you provide a compatibility fallback or a documented migration.
- Don’t overwrite explicit new settings with inferred legacy values.

2) Keep schema-driven configuration reachable in the UI
- If you skip a config property in a picker, only do so when there is a dedicated replacement control.
- If the skip removes the schema fallback path, add an explicit control (or adjust the skip condition) so users can still set the intended state.

3) Avoid global `process.env` as a workaround
- In shared-process code, changing `process.env` can affect other extensions/features indirectly.
- Prefer explicit dependency injection / request-scoped configuration plumbing.
- If you must set env vars in tests or isolated tooling, always clean up (e.g., in `afterEach`) to prevent leakage.

Example (compatibility migration pattern):
```ts
function readSandboxEnabled(config: IConfigurationService, log: ILogService): boolean {
  // New key
  const newEnabled = config.getValue<boolean>('chat.agent.sandbox.enabled');

  // Legacy key (explicit user opt-in)
  const legacy = config.getValue<boolean>('chat.agentHost.sdkSandbox.enabled');

  // Compatibility rule: use explicit new value if set; otherwise fall back to legacy.
  // (Implementation detail: treat `undefined` as “not explicitly set”.)
  if (newEnabled !== undefined) {
    return newEnabled;
  }

  if (legacy !== undefined) {
    log.debug('[Sandbox] Migrating legacy opt-in to new key');
    return legacy;
  }

  // Final default
  return false;
}
```

Example (env cleanup in tests):
```ts
afterEach(() => {
  delete process.env['COPILOT_API_URL'];
});
```

Applying this standard prevents silent behavior regressions after upgrades, ensures configuration is actually controllable by users, and reduces risk from hidden cross-feature coupling via `process.env`. 