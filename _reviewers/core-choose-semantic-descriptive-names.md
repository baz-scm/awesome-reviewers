---
title: Choose semantic descriptive names
description: 'Names should be clear, descriptive and follow consistent patterns. Choose
  names that accurately reflect the purpose and behavior of the code element:

  '
repository: vuejs/core
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 50769
---

Names should be clear, descriptive and follow consistent patterns. Choose names that accurately reflect the purpose and behavior of the code element:

1. Use semantic prefixes/suffixes that match established patterns:
   - State flags should use consistent prefixes (e.g., `isActivated` not `deactive`)
   - Type names should start with uppercase (e.g., `PluginParam` not `pluginParam`)
   - Internal implementations should use descriptive suffixes (e.g., `ComputedRefImpl` not `_ComputedRef`)

2. Pick clear, unambiguous names that convey intent:
   - Prefer descriptive names over abbreviated ones (e.g., `immediate` over `runOnce`)
   - Use complete words rather than shortened forms
   - Follow framework conventions (e.g., `VNodeKey` over `VKey`)

Example:
```ts
// Bad
class _ComputedRef {
  isDeactive: boolean
  runOnce: boolean
}

// Good
class ComputedRefImpl {
  isActivated: boolean
  immediate: boolean
}
```