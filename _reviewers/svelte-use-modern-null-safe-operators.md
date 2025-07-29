---
title: use modern null-safe operators
description: Prefer modern JavaScript null-safe operators over verbose conditional
  checks to improve code readability and prevent null-related errors. Use optional
  chaining (?.) for safe property access, nullish coalescing (??) for default values,
  and nullish coalescing assignment (??=) for lazy initialization.
repository: sveltejs/svelte
label: Null Handling
language: JavaScript
comments_count: 9
repository_stars: 83580
---

Prefer modern JavaScript null-safe operators over verbose conditional checks to improve code readability and prevent null-related errors. Use optional chaining (?.) for safe property access, nullish coalescing (??) for default values, and nullish coalescing assignment (??=) for lazy initialization.

**Key patterns to adopt:**

1. **Optional chaining for safe property access:**
```javascript
// Instead of verbose null checks
if (reaction.parent !== null && (reaction.parent.f & DERIVED) !== 0)

// Use optional chaining
if ((reaction.parent?.f & DERIVED) !== 0)
```

2. **Nullish coalescing for default values:**
```javascript
// Instead of logical OR
parent: parent_derived || active_effect

// Use nullish coalescing to handle only null/undefined
parent: parent_derived ?? active_effect
```

3. **Nullish coalescing assignment for lazy initialization:**
```javascript
// Instead of separate checks and assignments
if (to_animate === undefined) to_animate = new Set();
to_animate.add(item);

// Use nullish coalescing assignment
(to_animate ??= new Set()).add(item);
```

4. **Optional chaining for method calls:**
```javascript
// Instead of conditional calls
if (handler) {
    return handler.call(this, event);
}

// Use optional chaining
return handler?.call(this, event);
```

These operators provide cleaner, more expressive code while maintaining the same null-safety guarantees. They're particularly valuable in complex expressions where traditional null checks would require nested conditionals or temporary variables.