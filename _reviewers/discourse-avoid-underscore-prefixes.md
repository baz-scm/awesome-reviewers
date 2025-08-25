---
title: avoid underscore prefixes
description: 'Do not use underscore prefixes (`_`) for private or internal methods
  and properties. The team consensus is to avoid this naming convention. Instead,
  use one of these alternatives:'
repository: discourse/discourse
label: Naming Conventions
language: JavaScript
comments_count: 3
repository_stars: 44898
---

Do not use underscore prefixes (`_`) for private or internal methods and properties. The team consensus is to avoid this naming convention. Instead, use one of these alternatives:

1. **Remove the prefix entirely** for methods that don't need to be explicitly marked as private
2. **Use proper private syntax** with `#` prefix for truly private class members

**Examples:**

❌ Avoid:
```javascript
_isInLightMode() {
  return this.interfaceColor.colorModeIsLight;
}

_getUserColorSchemeDifferences() {
  // implementation
}
```

✅ Prefer:
```javascript
// Option 1: Remove prefix
isInLightMode() {
  return this.interfaceColor.colorModeIsLight;
}

// Option 2: Use proper private syntax
#getUserColorSchemeDifferences() {
  // implementation
}

// Option 3: Convert to getter when appropriate
get userColorSchemeDifferences() {
  // implementation
}
```

This convention improves code clarity and follows modern JavaScript standards while maintaining team consistency.