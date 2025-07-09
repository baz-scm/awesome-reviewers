---
title: Code example consistency
description: Ensure code examples in documentation and comments are syntactically
  correct and properly marked with the appropriate language identifier. This maintains
  a professional appearance and prevents readers from copying incorrect code.
repository: vitejs/vite
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 74031
---

Ensure code examples in documentation and comments are syntactically correct and properly marked with the appropriate language identifier. This maintains a professional appearance and prevents readers from copying incorrect code.

Key guidelines:
- Match language markers to the syntax used (e.g., use ```ts for TypeScript syntax with generics)
- Include all necessary syntax elements like commas and semicolons
- Avoid mixing TypeScript and JavaScript syntax in examples marked as plain JavaScript

Example - INCORRECT:
```js
function myPlugin() {
  const state = new Map<Environment, { count: number }>()
  return {
    name: 'my-plugin',
    buildStart() {
      state.set(this.environment, { count: 0 })
    // Missing comma here!
    transform(code) {
      // ...
    }
  }
}
```

Example - CORRECT:
```ts
function myPlugin() {
  const state = new Map<Environment, { count: number }>()
  return {
    name: 'my-plugin',
    buildStart() {
      state.set(this.environment, { count: 0 })
    }, // Proper comma after function
    transform(code) {
      // ...
    }
  }
}
```

Or alternatively with plain JS:
```js
function myPlugin() {
  const state = new Map()
  return {
    name: 'my-plugin',
    buildStart() {
      state.set(this.environment, { count: 0 })
    },
    transform(code) {
      // ...
    }
  }
}
```