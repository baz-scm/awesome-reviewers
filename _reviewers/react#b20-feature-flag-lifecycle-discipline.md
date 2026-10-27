---
title: Feature flag lifecycle discipline
description: Feature flags must be managed consistently through their full lifecycle.
  Before removing a flag, first roll it out by enabling it everywhere (including OSS
  and all forks) so it can be safely reverted if something breaks; never delete a
  flag outright without this intermediate step. When a flag isn't relevant to a particular
  environment/renderer, still set it...
repository: facebook/react#b20
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 251895
---

Feature flags must be managed consistently through their full lifecycle. Before removing a flag, first roll it out by enabling it everywhere (including OSS and all forks) so it can be safely reverted if something breaks; never delete a flag outright without this intermediate step. When a flag isn't relevant to a particular environment/renderer, still set it to a definite value (not left ambiguous) so future maintainers know it's safe to remove later.

When code depends on a flag-gated capability (e.g. a function only callable when a flag is on), gate every call site consistently — don't guard some usages and leave others unguarded. Keep the flag check at the top level of a block rather than scattered inside nested branches, so the whole block is dead-code-eliminated correctly in production builds:

```js
// Good: gate the whole block at the top level
if (enableAsyncDebugInfo) {
  const debugValue = moduleObject == null ? undefined : moduleObject.default;
  resolveDebugValue(debugValue);
  ioInfo.value.status = 'fulfilled';
  ioInfo.value.value = debugValue;
}

// Bad: only part of the logic is gated, rest relies on indirect conditions
const debugValue = moduleObject == null ? undefined : moduleObject.default;
resolveDebugValue(debugValue); // only callable when enableAsyncDebugInfo is true
```

Applying this consistently avoids broken builds when a flag is toggled, preserves proper dead-code elimination, and makes it clear when a flag is safe to remove.</description>
