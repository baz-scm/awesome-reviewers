---
title: "Consistent Fastify Package Naming and References"
description: "When implementing code using the Fastify package in TypeScript, it is important to use consistent and accurate naming conventions for Fastify-related references: always use the actual Fastify package name, use correct Fastify terminology and casing, and organize Fastify-related imports and references alphabetically."
repository: "fastify/fastify"
label: "Fastify"
language: "TypeScript"
comments_count: 2
repository_stars: 34000
---

When implementing code using the Fastify package in TypeScript, it is important to use consistent and accurate naming conventions for Fastify-related references:

- Always use the actual Fastify package name (`fastify`) rather than referring to the Fastify repository or other informal names.
- When referencing Fastify types, plugins, or other Fastify-specific concepts, use the correct Fastify terminology and casing (e.g. `FastifyInstance`, `fastify.get()`).
- Organize Fastify-related imports and references alphabetically to maintain consistency and make the code easier to navigate.

Example:
```typescript
// Preferred: Using the correct Fastify package name and terminology
import fastify, { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';

// Instead of informal references
import { createFastifyApp } from 'my-fastify-utils';

// Preferred: Alphabetized Fastify imports
import { FastifyPluginAsync } from 'fastify';
import fastifyAuth from '@fastify/auth';
import fastifyCors from '@fastify/cors';
```

Following these conventions will improve the maintainability of your Fastify-based codebase and make it easier for other developers to understand and work with the Fastify package correctly.