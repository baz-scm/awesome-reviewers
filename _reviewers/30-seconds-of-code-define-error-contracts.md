---
title: Define error contracts
description: 'When handling invalid input or terminal conditions, explicitly define
  and implement your error-handling contract. Avoid “surprising exits” (e.g., returning
  `false` or silently stopping) unless it’s part of the documented API. Either:'
repository: 30-seconds/30-seconds-of-code
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 129334
---

When handling invalid input or terminal conditions, explicitly define and implement your error-handling contract. Avoid “surprising exits” (e.g., returning `false` or silently stopping) unless it’s part of the documented API. Either:
- **Fail loudly**: let errors throw so callers can handle them, or
- **Fail explicitly**: catch and return a clear, documented sentinel (e.g., `undefined`).

Example (consistent, explicit contract):
```js
// Strategy 1: fail explicitly
const toEnglishDate = (time) => {
  try {
    return new Date(time).toISOString().split('T')[0].replace(/-/g, '/');
  } catch {
    return undefined; // documented sentinel
  }
};

// Strategy 2: fail loudly (caller decides)
const toEnglishDateOrThrow = (time) =>
  new Date(time).toISOString().split('T')[0].replace(/-/g, '/');
```

Apply the same idea to async chains: if the list ends or an element is missing, treat it as an intentional part of the function’s contract (document it) or let it throw—don’t hide the problem behind an unexpected return value.