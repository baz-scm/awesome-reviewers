---
title: Cache invariant computations
description: Avoid repeatedly computing values that don't change frequently. For data
  structures, maps, or validation schemas used in hot paths, initialize them once
  at module scope rather than recreating them on every function call.
repository: elie222/inbox-zero
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 8267
---

Avoid repeatedly computing values that don't change frequently. For data structures, maps, or validation schemas used in hot paths, initialize them once at module scope rather than recreating them on every function call.

**Examples:**

Instead of:
```typescript
function isValidEmail(email: string): boolean {
  return z.string().email().safeParse(email).success;
}
```

Prefer:
```typescript
const emailSchema = z.string().email();

function isValidEmail(email: string): boolean {
  return emailSchema.safeParse(email).success;
}
```

For mappings used frequently:
```typescript
// Bad: Recreates mapping on every call
export function getSubscriptionTier(priceId: string): Tier | null {
  for (const [tier, config] of Object.entries(PRICE_CONFIG)) {
    if (config.priceId === priceId) return tier as Tier;
  }
  return null;
}

// Good: Cache mapping once
const PRICE_ID_TO_TIER = Object.entries(PRICE_CONFIG).reduce(
  (acc, [tier, cfg]) => {
    if (cfg.priceId) acc[cfg.priceId] = tier as Tier;
    return acc;
  },
  {} as Record<string, Tier>
);

export function getSubscriptionTier(priceId: string): Tier | null {
  return PRICE_ID_TO_TIER[priceId] ?? null;
}
```

For frequently accessed data that rarely changes, consider Redis caching:
```typescript
// Get provider for account (provider never changes after account creation)
async function getAccountProvider(accountId: string) {
  const cachedProvider = await redis.get(`account-provider:${accountId}`);
  if (cachedProvider) return cachedProvider;
  
  const provider = await prisma.account.findUnique({
    where: { id: accountId },
    select: { provider: true }
  });
  
  await redis.set(`account-provider:${accountId}`, provider, "EX", 86400);
  return provider;
}
```

This optimization reduces memory allocations, CPU usage, and can significantly improve performance in hot paths.