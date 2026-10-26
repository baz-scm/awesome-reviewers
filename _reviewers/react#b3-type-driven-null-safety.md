---
title: Type-Driven Null Safety
description: 'When a value may be null/undefined or lacks the expected shape, don’t
  access members directly. Instead: (1) derive the correct runtime “owner/root” object
  for the property you need, (2) narrow (or early-return) based on node/object type
  before reading, and (3) use consistent null checks and type-safe initialization.'
repository: facebook/react#b3
label: Null Handling
language: JavaScript
comments_count: 8
repository_stars: 251883
---

When a value may be null/undefined or lacks the expected shape, don’t access members directly. Instead: (1) derive the correct runtime “owner/root” object for the property you need, (2) narrow (or early-return) based on node/object type before reading, and (3) use consistent null checks and type-safe initialization.

**Do**
- Compute the correct receiver from runtime context (e.g., use a helper that returns the right `DocumentOrShadowRoot`), then read the property.
- Guard/branch before property access:
  - early return when a ref/portal container can be missing
  - optional chaining when you only need the value
- Initialize optional variables to the correct nullable type rather than using broader `void | T` patterns.
- Choose null-check style intentionally:
  - use `value == null` if you mean “null OR undefined”
  - use `value === null` if you mean only null

**Example**
```js
// Prefer correct owner/root derivation before reading .activeElement
const activeElementRoot = getOwnerDocumentFromRootContainer(parentInstanceOrContainer);
const activeElement: ?Element = activeElementRoot.activeElement;
if (activeElement == null) {
  return;
}

// Guard before calling methods on possibly-null strings/values
const displayName = this.showNames
  ? agent.getComponentNameForHostInstance(node)
  : null;
if (displayName != null && displayName.startsWith('Forget(')) {
  // safe
}

// Early return when a ref can be null
const menu = ref.current;
if (menu == null) {
  return;
}
```

Applying this standard reduces crashes like calling methods on null, avoids reading properties from the wrong object type, and prevents type confusion from “casting past” nullability.