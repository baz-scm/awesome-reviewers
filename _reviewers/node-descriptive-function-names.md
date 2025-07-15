---
title: Descriptive function names
description: Function and method names should precisely describe their purpose and
  behavior. Choose names that explicitly communicate what the function does, including
  any special conditions or behaviors.
repository: nodejs/node
label: Naming Conventions
language: JavaScript
comments_count: 4
repository_stars: 112178
---

Function and method names should precisely describe their purpose and behavior. Choose names that explicitly communicate what the function does, including any special conditions or behaviors.

Key guidelines:
- Name methods to reflect their exact purpose (e.g., use `toJSON()` instead of `toJson()` for JSON serialization)
- Be specific about the action being performed (e.g., prefer `setupBindings()` over `setupInstance()` when setting up bindings rather than an instance)
- Include conditions in the name when applicable (e.g., `maybeEmitDeprecationWarning` or `emitDeprecationWarningIfAlgoIsShake` instead of just `emitDeprecationWarning`)
- Maintain consistent naming patterns across similar APIs (e.g., use `enable()`/`disable()` if that's the established pattern for similar functionality)

Example:
```javascript
// ❌ Poor naming - ambiguous about purpose and behavior
function setup(instance, memory) {
  // Implementation
}

// ✅ Better naming - clearly describes what's being set up
function setupBindings(instance, { memory = instance.exports.memory } = {}) {
  // Implementation
}

// ❌ Poor naming - doesn't indicate conditional behavior
const emitDeprecationWarning = getDeprecationWarningEmitter();

// ✅ Better naming - indicates the warning is conditional
const maybeEmitDeprecationWarning = getDeprecationWarningEmitter();
```