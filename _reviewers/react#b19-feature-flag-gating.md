---
title: Feature flag gating
description: 'When introducing or using a feature flag, gate the entire logical block
  at the top level rather than scattering the check inline or only guarding a nested
  call. This keeps dead-code elimination correct and the code readable:'
repository: facebook/react#b19
label: Configurations
language: JavaScript
comments_count: 8
repository_stars: 251893
---

When introducing or using a feature flag, gate the entire logical block at the top level rather than scattering the check inline or only guarding a nested call. This keeps dead-code elimination correct and the code readable:

```js
// Preferred
if (enableFragmentRefsTextNodes) {
  if (child.tag === HostText) {
    // ...
  }
}

// Avoid
if (resolvedAlignToTop && enableFragmentRefsTextNodes && child.tag === HostText) {
  // ...
}
```

If a block calls a function or reads a value that is itself only valid/implemented when a flag is enabled (e.g. `resolveDebugValue` under `enableAsyncDebugInfo`), gate the surrounding block too, even if the flag isn't yet universally enabled — don't rely on indirect guarantees. Prefer gating in the implementation (e.g. `ReactFlightServer.js`/`ReactFlightClient.js`) rather than at every entrypoint/call site unless there's a concrete reason to duplicate the check.

During rollout, default flags to enabled in all forks/configs (including platforms like React Native or test environments) unless there is a specific reason to keep them off; leaving a flag arbitrarily disabled blocks future cleanup/removal and obscures whether it's safe to delete. When fully removing a flag, first flip it to enabled everywhere (including OSS) as a separate step before deleting the flag, so it can be reverted if it causes regressions.

Keep related build/runtime settings consistent across similar configurations (e.g. all browser bundles should minify prod error codes the same way).

In tests, prefer the `gate('flagName')` helper over importing the raw feature-flags module directly, to keep flag-dependent test behavior consistent and discoverable.</description>
