---
title: Separate language documentation
description: Keep general API documentation language-agnostic while placing language-specific
  examples and patterns in dedicated files. This improves maintainability and prevents
  redundancy in the codebase.
repository: axios/axios
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 107146
---

Keep general API documentation language-agnostic while placing language-specific examples and patterns in dedicated files. This improves maintainability and prevents redundancy in the codebase.

For example, when documenting Fastify decorators:

```js
// Good: In general docs (Decorators.md)
// Concise, language-agnostic documentation
fastify.decorateRequest('user', null)

fastify.addHook('preHandler', async (req, reply) => {
  req.setDecorator('user', 'Bob Dylan')
})

// Good: In TypeScript docs (TypeScript.md)
// TypeScript-specific patterns and examples
const session = request.getDecorator<ISession>('session')
reply.send(session)
```

When documentation content moves to a more appropriate location, remove it from the original source to avoid duplication. This ensures that readers find the most relevant examples in the expected places and prevents conflicting information as the codebase evolves.

## Discussions

