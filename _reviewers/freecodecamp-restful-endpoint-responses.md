---
title: RESTful endpoint responses
description: 'When designing API routes, make the HTTP method and response contract
  match the operation’s intent and the client’s needs.


  - Pick the correct verb: use DELETE for destructive/reset-like removal semantics
  when appropriate, and reserve POST for creation/processing actions.'
repository: freeCodeCamp/freeCodeCamp
label: API
language: TypeScript
comments_count: 2
repository_stars: 444449
---

When designing API routes, make the HTTP method and response contract match the operation’s intent and the client’s needs.

- Pick the correct verb: use DELETE for destructive/reset-like removal semantics when appropriate, and reserve POST for creation/processing actions.
- Choose a standard response:
  - If nothing needs to be consumed by the client, return `204 No Content`.
  - If the client needs confirmation, return either the updated resource (e.g., updated `user`) or a minimal, explicit summary of what changed (e.g., which items were removed).
- Avoid returning payloads that are arbitrary or unlikely to be used; keep the response minimal and purposeful.

Example pattern:
```ts
fastify.delete('/account/reset-module', {
  schema: schemas.resetModule
}, async (req, reply) => {
  // ...remove/reset items
  return reply.code(204);
});

// OR if the client needs a summary:
return {
  blockId,
  completedChallengesRemoved,
  savedChallengesRemoved,
  partiallyCompletedChallengesRemoved
};
```