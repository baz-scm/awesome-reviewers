---
title: Feature flag rollout hygiene
description: 'When changing feature flags or config-driven code paths, apply three
  rules: (1) safe rollout/removal, (2) consistent gating boundaries, and (3) consistent
  testing/wiring.'
repository: facebook/react#b17
label: Configurations
language: JavaScript
comments_count: 8
repository_stars: 251891
---

When changing feature flags or config-driven code paths, apply three rules: (1) safe rollout/removal, (2) consistent gating boundaries, and (3) consistent testing/wiring.

1) Roll out broadly before removal
- If a flag is being enabled/removed, first enable it everywhere (including OSS) and keep the flag present during the rollout so it can be disabled quickly if it breaks.
- Don’t disable flags “because the renderer doesn’t use it”; leaving it enabled across forks/non-using environments avoids getting blocked later when deciding if it’s safe to remove.

2) Gate correctly and consistently
- Prefer gating in the implementation where the option/feature is consumed (not in entrypoints), unless the entrypoint is truly the source of the behavior.
- If a helper/function is only valid when a flag is enabled, gate the entire surrounding block—don’t rely on partial guarding.
- Use consistent, minimal gating structure for readability:

```js
// Good: whole block guarded by the feature flag
if (enableSomeFeature) {
  if (child.tag === HostText) {
    // do feature-specific behavior
  }
}
```

- Apply explicit dev-only guards where appropriate for debug/profiling data paths, and avoid doing work in branches that aren’t reachable in dev.

3) Test and wire flags via the standard mechanism
- In tests, gate behavior using the project’s standard flag-gating helper (e.g., `gate('flag')`) rather than importing feature-flag modules directly.
- Verify the flag is correctly connected in the relevant dynamic/bundled entry (some flags may only apply when dynamically imported).