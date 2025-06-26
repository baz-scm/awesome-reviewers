---
title: "Documentation reflects reality"
description: "Always ensure documentation accurately represents the actual code behavior and implementation details. Include important contextual information such as platform-specific limitations, explanations for deprecated features with recommended alternatives, precise descriptions of function parameters and behaviors, and concise, merged code examples to demonstrate functionality."
repository: "axios/axios"
label: "Documentation"
language: "Markdown"
comments_count: 5
repository_stars: 107000
---

Always ensure documentation accurately represents the actual code behavior and implementation details. Include important contextual information such as:

1. Platform-specific limitations (e.g., "Node only" features)
2. Explanations for deprecated features with recommended alternatives
3. Precise descriptions of function parameters and behaviors
4. Concise, merged code examples to demonstrate functionality

When documenting APIs, verify that your descriptions match the actual implementation rather than the intended design. For example, if a function behaves differently than originally designed, update the documentation to reflect the actual behavior:

```js
// INCORRECT DOCUMENTATION
// `validateStatus` defines whether to resolve or reject the promise for a given
// HTTP response status code. If `validateStatus` returns `true` (or is set to `null`
// or `undefined`), the promise will be resolved; otherwise, the promise will be rejected.

// CORRECT DOCUMENTATION
// `validateStatus` defines whether to resolve or reject the promise for a given
// HTTP response status code. If `validateStatus` returns `true` (or is set to `null`), 
// the promise will be resolved; otherwise, the promise will be rejected.
```

For deprecated features, clearly indicate:
```
~~Concurrency~~
Deprecated. Use `Promise.all` to replace them.
```

Keep documentation concise by consolidating related code examples when possible.