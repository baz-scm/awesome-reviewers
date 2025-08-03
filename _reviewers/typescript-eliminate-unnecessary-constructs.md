---
title: Eliminate unnecessary constructs
description: Remove redundant or unnecessary code constructs to improve readability
  and maintainability. This includes avoiding empty blocks, blocks containing only
  empty statements, and unnecessary variable declarations that don't enhance code
  clarity.
repository: microsoft/typescript
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 105378
---

Remove redundant or unnecessary code constructs to improve readability and maintainability. This includes avoiding empty blocks, blocks containing only empty statements, and unnecessary variable declarations that don't enhance code clarity.

Example (before):
```javascript
try {
    const resource = __addDisposableResource(env, resource_1, true);
    {
        ; // Empty block with just a semicolon
    }
}

// Or unnecessary variables:
__assign = Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
```

Example (after):
```javascript
try {
    const resource = __addDisposableResource(env, resource_1, true);
    // No empty block
}

// Simplified variables:
__assign = Object.assign || function(t) {
    for (var i = 1; i < arguments.length; i++) {
        var source = arguments[i];
        for (var key in source) {
            if (Object.prototype.hasOwnProperty.call(source, key)) {
                t[key] = source[key];
            }
        }
    }
    return t;
};
```