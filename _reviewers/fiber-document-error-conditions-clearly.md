---
title: Document error conditions clearly
description: Always provide clear documentation for error conditions, unsafe usage
  patterns, and failure scenarios in API documentation. Include explicit warnings
  about potential data races, undefined behavior, and error propagation to help developers
  avoid common pitfalls.
repository: gofiber/fiber
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 37560
---

Always provide clear documentation for error conditions, unsafe usage patterns, and failure scenarios in API documentation. Include explicit warnings about potential data races, undefined behavior, and error propagation to help developers avoid common pitfalls.

When documenting methods that can lead to unsafe states or have specific error behaviors, use prominent warning blocks and describe the exact consequences:

```markdown
**Close** releases both the associated `Request` and `Response` objects back to their pools.

⚠️ **WARNING**: After calling `Close`, any attempt to use the request or response may result in data races or undefined behavior. Ensure all processing is complete before closing.
```

For systems with error propagation, clearly state the behavior:

```markdown
If any request hook returns an error, the request is interrupted and the error is returned immediately.
```

This practice helps developers understand failure scenarios upfront, enabling them to write more robust error handling code and avoid runtime issues.