---
title: Use modern nullish operators
description: When dealing with potentially null or undefined values, use optional
  chaining (`?.`) and nullish coalescing (`??`) operators instead of verbose conditionals.
  These operators make code more readable, concise, and prevent null reference errors.
repository: nodejs/node
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 112178
---

When dealing with potentially null or undefined values, use optional chaining (`?.`) and nullish coalescing (`??`) operators instead of verbose conditionals. These operators make code more readable, concise, and prevent null reference errors.

```javascript
// Verbose and error-prone
if (object && object.property) {
  value = object.property;
} else {
  value = defaultValue;
}

// Concise and safe
value = object?.property ?? defaultValue;
```

In real-world code, these operators simplify common patterns:

```javascript
// From discussion #1: Safely access property with fallback
innerOk(this?.ok ?? ok, args.length, ...args);

// From discussion #13: Conditional assignment with fallback
this.secureOptions = secureOptions || undefined;

// From discussion #15: Lazy loading with nullish assignment
inspect ??= require('util').inspect;
return inspect;
```

These operators are particularly valuable for:
- Safely accessing deeply nested properties without verbose checks
- Setting default values when null or undefined is encountered
- Simplifying conditional logic around nullable values
- Reducing boilerplate code for null safety

Remember that optional chaining short-circuits when a reference is nullish, while nullish coalescing only falls back when the left side is specifically `null` or `undefined` (not other falsy values like `0` or `''`).