---
title: Use definite assignment assertions
description: When you're certain a value will be initialized but TypeScript can't
  infer this, use the definite assignment assertion operator (`!`) instead of `as
  any` or suppressing type errors. This maintains type safety while avoiding unnecessary
  null checks throughout your codebase.
repository: cloudflare/agents
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 2312
---

When you're certain a value will be initialized but TypeScript can't infer this, use the definite assignment assertion operator (`!`) instead of `as any` or suppressing type errors. This maintains type safety while avoiding unnecessary null checks throughout your codebase.

Avoid this pattern:
```typescript
// Creates unnecessary undefined checks everywhere
#agent: Agent<Env, State> | undefined;

// Or suppressing valid type concerns
// @ts-expect-error TODO: fix this type error
await this._drainStream(response.body);

// Or forcing types unsafely  
}) as any
```

Instead, use definite assignment assertions when you know the value will be there:
```typescript
// Tells TypeScript "trust us, it'll always be there"
#agent: Agent<Env, State>!;
```

Or add proper null checks when the value might actually be null:
```typescript
// When the value could legitimately be null/undefined
if (response.body) {
  const reader = response.body.getReader();
  // ... handle the stream
}
```

This approach maintains TypeScript's null safety benefits while eliminating false positives that lead to code pollution or unsafe type assertions.