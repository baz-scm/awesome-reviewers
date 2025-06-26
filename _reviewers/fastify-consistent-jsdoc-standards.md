---
title: "Consistent JSDoc standards"
description: "Document all public APIs and significant internal functions with comprehensive JSDoc comments that include accurate descriptions, parameter and return types, and any notable side effects. Follow standard JSDoc format conventions consistently across the codebase."
repository: "fastify/fastify"
label: "Documentation"
language: "JavaScript"
comments_count: 5
repository_stars: 34000
---

Document all public APIs and significant internal functions with comprehensive JSDoc comments that include accurate descriptions, parameter and return types, and any notable side effects. Follow standard JSDoc format conventions consistently across the codebase.

When documenting functions:

- Include clear descriptions of purpose and behavior:
```js
/**
 * Leverage light-my-request package to injects a fake HTTP request/response
 * into Fastify for simulating server logic, writing tests, or debugging.
 *
 * Warning: if the server is not yet "ready," this utility will force
 * the server into the ready state.
 *
 * @see {@link https://github.com/fastify/light-my-request}
 */
fastify.inject = setupInject(fastify, {
```

- Use proper JSDoc tag formats with types and descriptions:
```js
/**
 * @param {object} serverOptions the fastify server options
 * @returns {object} New logger instance, inheriting all parent bindings,
 * with child bindings added.
 */
```

- For utility functions, especially those used in tests, include explanation of parameters and execution flow:
```js
/**
 * Executes an array of asynchronous steps in sequence. Each step is a function
 * that takes a `next` callback as its argument. The `next` callback must be
 * called to proceed to the next step.
 *
 * @param {Function[]} steps - An array of functions representing the steps to execute.
 */
```

Maintain consistent formatting across all JSDoc comments. This improves code readability, makes API documentation generation more effective, and helps new developers understand the codebase more quickly.