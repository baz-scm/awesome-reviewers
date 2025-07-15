---
title: "Check property existence first"
description: "Always verify that an object and its properties exist before accessing them to prevent 'cannot read property of undefined/null' errors. This is especially important when dealing with objects that might come from different build environments or third-party libraries."
repository: "facebook/react"
label: "Null Handling"
language: "JavaScript"
comments_count: 3
repository_stars: 237000
---

Always verify that an object and its properties exist before accessing them to prevent "cannot read property of undefined/null" errors. This is especially important when dealing with objects that might come from different build environments (dev vs. production) or third-party libraries.

There are two common approaches:
1. Using a falsy check when null and undefined are both invalid: `if (!obj)` or `if (!obj.property)`
2. Using explicit checks when you need to distinguish between different falsy values: `if (obj === undefined)` or `if (obj.property === null)`

**Example - Before:**
```javascript
// Risky code that might fail
clonedElement._store.validated = oldElement._store.validated;
```

**Example - After:**
```javascript
// Safe code that checks existence first
if (oldElement._store && clonedElement._store) {
  clonedElement._store.validated = oldElement._store.validated;
}
```

This is particularly important in codebases where:
1. Components might be rendered in both development and production environments
2. You're integrating with third-party libraries that might have different property structures
3. Properties might be conditionally added to objects

Being proactive about property existence checks leads to more robust code and prevents unexpected runtime errors.