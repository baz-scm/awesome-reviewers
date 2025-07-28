---
title: validate before operations
description: Always explicitly check for null, undefined, or missing properties/methods
  before performing operations that could fail. JavaScript's loose typing and the
  fact that `typeof null === 'object'` can lead to runtime errors if values aren't
  validated first.
repository: facebook/react-native
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 123178
---

Always explicitly check for null, undefined, or missing properties/methods before performing operations that could fail. JavaScript's loose typing and the fact that `typeof null === 'object'` can lead to runtime errors if values aren't validated first.

Key patterns to implement:
- Check for null/undefined objects: `if (params == null) { return; }`
- Verify method existence: `if (typeof child.removeParent === 'function') { child.removeParent(this); }`
- Validate array elements: `if (_backPressSubscriptions[i] && _backPressSubscriptions[i]()) { ... }` or use optional chaining `_backPressSubscriptions[i]?.()`

This prevents common runtime errors and makes code more robust by handling edge cases where expected values or methods might not be present.