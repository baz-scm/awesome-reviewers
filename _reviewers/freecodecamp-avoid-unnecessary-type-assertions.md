---
title: Avoid Unnecessary Type Assertions
description: In route/controller code, don’t rely on repeated `as` casts to satisfy
  TypeScript—normalize/validate types once, then keep the rest of the logic strongly
  typed.
repository: freeCodeCamp/freeCodeCamp
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 444449
---

In route/controller code, don’t rely on repeated `as` casts to satisfy TypeScript—normalize/validate types once, then keep the rest of the logic strongly typed.

Apply this style rule:
- If you see patterns like `(value as unknown[]).filter(...)` or `filteredX as never`, it’s a formatting/readability smell.
- Replace them with a single typed normalization/helper (or adjust the Prisma/type definitions) so the filtered result already has the right shape.

Example (mimic the proposed approach):
```ts
// Normalize once to the correct element shape
const normalizeChallenges = (arr: unknown) => arr as Array<{ id: string }>;

const filteredCompletedChallenges = normalizeChallenges(user.completedChallenges)
  .filter(c => !challengeIdsToReset.includes(c.id));

await fastify.prisma.user.update({
  where: { id: req.user!.id },
  data: {
    completedChallenges: filteredCompletedChallenges,
  },
});
```