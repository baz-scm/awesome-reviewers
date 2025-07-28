---
title: Use null meaningfully
description: Choose between null and undefined based on semantic intent rather than
  convenience. Use null when operations can explicitly fail and you want to represent
  that failure state, allowing consumers to handle it appropriately. Use optional
  properties (?) when a value may simply not be provided or initialized.
repository: cline/cline
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 48299
---

Choose between null and undefined based on semantic intent rather than convenience. Use null when operations can explicitly fail and you want to represent that failure state, allowing consumers to handle it appropriately. Use optional properties (?) when a value may simply not be provided or initialized.

Avoid redundant null safety patterns when operations are guaranteed to succeed, as this can create unnecessary complexity and potential regressions.

Example:
```ts
// Good: null represents explicit failure state
interface ExtensionState {
  totalTasksSize: number | null  // null when operation fails
}

// Good: undefined represents uninitialized/optional state  
interface ComponentProps {
  targetSection?: string  // may not be provided
}

// Avoid: redundant fallback when find() will always succeed
const defaultTab = SETTINGS_TABS.find(tab => tab.id === "general")?.id ?? SETTINGS_TABS[0].id
```

This approach makes the code's intent clearer and helps consumers understand how to handle different null states appropriately.