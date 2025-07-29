---
title: API flexibility balance
description: When designing APIs, carefully balance simplicity for common use cases
  with flexibility for advanced scenarios. Consider whether to expose simple interfaces
  (strings, direct exports) that make typical usage ergonomic, or more flexible interfaces
  (objects, options parameters) that enable customization.
repository: sveltejs/svelte
label: API
language: JavaScript
comments_count: 4
repository_stars: 83580
---

When designing APIs, carefully balance simplicity for common use cases with flexibility for advanced scenarios. Consider whether to expose simple interfaces (strings, direct exports) that make typical usage ergonomic, or more flexible interfaces (objects, options parameters) that enable customization.

For return values, prefer simple types when most users need straightforward access, but consider objects when users need to combine or manipulate the data. For example, returning `htmlAttributes: "class=\"foo\" id=\"bar\""` makes simple insertion easy, while an object would better support merging with existing attributes.

For method parameters, design signatures that minimize boilerplate. Accept both single values and arrays rather than forcing callers to wrap single items: `method(value)` and `method([value1, value2])` instead of always requiring `method([value])`.

For extensibility, use options objects for functions that may grow additional parameters over time:

```javascript
// Instead of: migrate(source, filename)
// Use: migrate(source, { filename })
```

This allows future enhancements without breaking existing calls and keeps the API clean as requirements evolve.