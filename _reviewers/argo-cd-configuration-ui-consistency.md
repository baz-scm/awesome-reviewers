---
title: Configuration UI consistency
description: Ensure that configuration user interfaces accurately reflect the underlying
  configuration behavior and data structures. UI controls should provide clear, transparent
  mapping to the actual configuration values, including precedence rules and field
  relationships.
repository: argoproj/argo-cd
label: Configurations
language: TSX
comments_count: 2
repository_stars: 20149
---

Ensure that configuration user interfaces accurately reflect the underlying configuration behavior and data structures. UI controls should provide clear, transparent mapping to the actual configuration values, including precedence rules and field relationships.

When building configuration forms, avoid situations where:
- UI state doesn't match the backend configuration logic
- Users cannot understand which configuration fields are actually being used
- Form controls represent multiple backend states ambiguously

For example, if your backend has precedence rules like "ValuesObject takes precedence over Values", the UI should either:
1. Provide visual indication of which field is active
2. Consolidate the interface to use a single field consistently

```typescript
// Bad: UI checkbox maps to multiple backend states
const isEnabled = automated.enabled !== false; // Could be undefined, true, or false

// Better: Explicit handling of configuration states
const getAutoSyncState = (automated) => {
  if (automated.enabled === false) return 'disabled';
  if (automated.enabled === true) return 'enabled';
  return 'default-enabled'; // When enabled field is undefined
};
```

This prevents user confusion and ensures that configuration changes through the UI produce predictable results in the underlying system.