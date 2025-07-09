---
title: Provide actionable examples
description: Documentation should include concrete, executable code examples rather
  than vague instructions. Make your examples copy-paste ready with all necessary
  context and dependencies. When documenting features or APIs, show exactly how they
  should be used in practice.
repository: vercel/ai
label: Documentation
language: Other
comments_count: 3
repository_stars: 15590
---

Documentation should include concrete, executable code examples rather than vague instructions. Make your examples copy-paste ready with all necessary context and dependencies. When documenting features or APIs, show exactly how they should be used in practice.

For example, instead of just stating:
```ts
// Don't do this
// You can pass provider options as an argument
```

Provide a complete, executable example:
```ts
// Do this
const result = await embed({
  model: cohere.embedding('embed-english-v3.0'),
  input: 'Hello world',
  providerOptions: {
    cohere: {
      inputType: 'search_query'
    }
  }
});
```

For pre-release or alpha software, clearly state limitations and expectations (e.g., "not for production use", "subject to breaking changes"). Always aim to create documentation that developers can immediately implement without needing to figure out missing pieces.