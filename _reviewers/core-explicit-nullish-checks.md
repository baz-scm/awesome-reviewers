---
title: Explicit nullish checks
description: When checking for the absence of values, use explicit nullish checks
  rather than relying on JavaScript's falsy behavior. This prevents issues with valid
  falsy values like empty strings, zero, or false being treated as non-existent.
repository: vuejs/core
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 50769
---

When checking for the absence of values, use explicit nullish checks rather than relying on JavaScript's falsy behavior. This prevents issues with valid falsy values like empty strings, zero, or false being treated as non-existent.

**Bad:**
```javascript
// This will skip empty strings, zero, and false
if (vars[key]) {
  style.setProperty(`--${key}`, vars[key])
}

// Similarly problematic for numeric inputs
if (props.value) {
  el.setAttribute('value', props.value)
}
```

**Good:**
```javascript
// Handles empty strings correctly
if (vars[key] || vars[key] === '') {
  style.setProperty(`--${key}`, vars[key])
}

// Even better - explicitly checks for null/undefined
if (vars[key] !== undefined && vars[key] !== null) {
  style.setProperty(`--${key}`, vars[key])
}

// Or use loose equality for brevity when appropriate
if (props.value != null) {
  el.setAttribute('value', props.value)
}
```

Remember that `value == null` checks for both `null` and `undefined`, while `value === null` only checks for `null`. Choose the appropriate check based on your requirements. When handling form inputs, DOM properties, or CSS variables, be especially careful as empty strings and zero are often valid values that should be preserved.