---
title: Use modern syntax
description: 'Adopt modern JavaScript and Ember syntax patterns instead of legacy
  approaches to improve code readability and maintainability.


  Key modern patterns to use:'
repository: discourse/discourse
label: Code Style
language: Other
comments_count: 5
repository_stars: 44898
---

Adopt modern JavaScript and Ember syntax patterns instead of legacy approaches to improve code readability and maintainability.

Key modern patterns to use:

**Native private methods** - Use `#` prefix instead of underscore convention:
```javascript
// ❌ Legacy
_buildEventObject(from, to) {
  // implementation
}

// ✅ Modern
#buildEventObject(from, to) {
  // implementation  
}
```

**Boolean attributes** - Use proper boolean syntax instead of explicit true/false:
```handlebars
<!-- ❌ Legacy -->
<input disabled={{true}} />

<!-- ✅ Modern -->
<input disabled />
```

**Optional chaining** - Use `?.` for cleaner conditional calls:
```javascript
// ❌ Legacy
if (this.onBlur) {
  this.onBlur(this.normalize(this.hexValue));
}

// ✅ Modern  
this.onBlur?.(this.normalize(this.hexValue));
```

**Modern array methods** - Use `.at()` for array access:
```javascript
// ❌ Legacy
const lastWord = words[words.length - 1];

// ✅ Modern
const lastWord = words.at(-1);
```

These modern syntax patterns are now well-supported and provide cleaner, more expressive code that aligns with current JavaScript and Ember best practices.