---
title: Feature flag gating standards
description: 'When adding or modifying feature flags / env-based options, make gating
  consistent, safe, and easy to roll back.


  1) Roll out safely

  - Prefer “enable everywhere first” for new flags slated for rollout/removal. This
  lets you disable quickly if anything breaks in any build.'
repository: facebook/react#b11
label: Configurations
language: JavaScript
comments_count: 9
repository_stars: 251894
---

When adding or modifying feature flags / env-based options, make gating consistent, safe, and easy to roll back.

1) Roll out safely
- Prefer “enable everywhere first” for new flags slated for rollout/removal. This lets you disable quickly if anything breaks in any build.
- Keep the flag defined in all platform/renderer forks until you’ve verified removal is safe (avoid later uncertainty/blocking).

2) Guard the whole code path (not just callees)
- If a helper is only valid under a flag, gate the entire surrounding block so the code is never partially executed when the flag is off.
- Don’t add redundant guards where the function is provably unreachable in that environment.

3) Choose one gating location strategy
- Common pattern: guard option/flag reads inside the implementation (and pass values through from entrypoints) rather than wrapping every entrypoint with flags—unless the entrypoint behavior itself must change.

4) Standardize gating style
- Gate by feature flag first, then apply any secondary conditions inside:

```js
if (enableSomeFeature) {
  if (child.tag === HostText) {
    // ...
  }
}
```

5) Use the standard flag gate mechanism in tests
- In tests, use the project’s standard `gate('flagName')` approach rather than importing feature-flag modules directly.

Applying these rules improves clarity (what executes when), avoids accidental partial execution, reduces dead-code risk, and makes rollouts/removals predictable.