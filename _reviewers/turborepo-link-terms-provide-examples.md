---
title: Link terms, provide examples
description: When writing technical documentation, link to related concepts the first
  time they are mentioned, and include concrete examples to illustrate complex features
  or functionality.
repository: vercel/turborepo
label: Documentation
language: Other
comments_count: 2
repository_stars: 28115
---

When writing technical documentation, link to related concepts the first time they are mentioned, and include concrete examples to illustrate complex features or functionality.

When introducing a term or concept:
1. Link to its definition or more detailed explanation on its first occurrence
2. Include practical examples when explaining features or configurations
3. Consider the reader's perspective - what might be unclear to someone unfamiliar with the system?

**Example:**

```markdown
// Less helpful:
Turborepo's Environment Modes allow you to control which environment variables are available to a task at runtime.

// More helpful:
[Turborepo's Environment Modes](/repo/docs/core-concepts/environment-variables) allow you to control which environment variables are available to a task at runtime. For example:

```json
{
  "envMode": "strict",
  "env": ["API_KEY", "DEBUG"]
}
```
```

This approach helps readers immediately access relevant context without needing to search for it, and concrete examples make abstract concepts easier to understand and implement.