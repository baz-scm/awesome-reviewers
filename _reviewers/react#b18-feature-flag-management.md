---
title: Feature flag management
description: When adding or changing behavior behind a feature flag, gate the *entire*
  dependent code path with that flag, not just the inner logic. If a function or block
  only makes sense (or is only safely callable) when a flag is enabled, wrap the whole
  block in the flag check rather than relying on it being implied by some other condition
  — this keeps the code...
repository: facebook/react#b18
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 251889
---

When adding or changing behavior behind a feature flag, gate the *entire* dependent code path with that flag, not just the inner logic. If a function or block only makes sense (or is only safely callable) when a flag is enabled, wrap the whole block in the flag check rather than relying on it being implied by some other condition — this keeps the code correct, aids dead-code-elimination in flag-disabled builds, and makes intent obvious to readers. Keep gating style consistent across call sites (e.g. don't dev-gate one call to a helper and leave a sibling call ungated):

```js
// Prefer this:
if (enableFragmentRefsTextNodes) {
  if (child.tag === HostText) {
    // ...
  }
}

// Not this (mixes the flag check into an unrelated condition):
if (enableFragmentRefsTextNodes && child.tag === HostText) {
  // ...
}
```

Separately, follow a staged rollout process for flags rather than jumping straight to enabling or removing them. Before removing a flag, first flip it on everywhere in OSS (not just experimental builds) so it can be reverted quickly if something breaks; only delete the flag and dead branches once it has proven stable. When flipping a flag on by default, prefer enabling it fully (rather than gating behind `__EXPERIMENTAL__` only) once it has been validated in production, since full enablement gives a clear, fast revert path if issues surface — but this should be a deliberate decision backed by production signal, not a shortcut around the normal flag lifecycle (add flag off by default → enable in dev/experimental → validate in production → enable everywhere → remove flag).</description>
</invoke>
