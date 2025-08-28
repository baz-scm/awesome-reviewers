---
title: Improve documentation clarity
description: Write clear, accessible, and consistent documentation by using descriptive
  link text and providing complete, realistic examples. Avoid generic link text like
  "here" or "click here" - instead, describe what the link leads to. Ensure code examples
  are comprehensive and consistent across all documentation.
repository: better-auth/better-auth
label: Documentation
language: Other
comments_count: 2
repository_stars: 19651
---

Write clear, accessible, and consistent documentation by using descriptive link text and providing complete, realistic examples. Avoid generic link text like "here" or "click here" - instead, describe what the link leads to. Ensure code examples are comprehensive and consistent across all documentation.

For links, replace generic text:
```markdown
// Avoid
Read more [here](https://redis.io/).

// Prefer  
Read more [about Redis here](https://redis.io/).
```

For code examples, provide realistic, complete configurations:
```ts
// Avoid incomplete examples
connectionString: "redis://localhost:6379"

// Prefer complete, realistic examples
connectionString: "redis://user:password@localhost:6379"
```

This approach improves accessibility for screen readers and other assistive technologies while ensuring developers have practical, working examples they can adapt to their needs.