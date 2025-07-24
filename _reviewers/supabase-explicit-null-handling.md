---
title: Explicit null handling
description: 'Use explicit patterns when dealing with potentially null or undefined
  values to prevent runtime errors and improve code clarity:


  1. **Mark optional properties with the `?` operator** in TypeScript interfaces when
  values might be undefined:'
repository: supabase/supabase
label: Null Handling
language: TSX
comments_count: 3
repository_stars: 86070
---

Use explicit patterns when dealing with potentially null or undefined values to prevent runtime errors and improve code clarity:

1. **Mark optional properties with the `?` operator** in TypeScript interfaces when values might be undefined:

```typescript
// Bad
interface GuideArticleProps {
  content: string
  mdxOptions: SerializeOptions
}

// Good
interface GuideArticleProps {
  content?: string
  mdxOptions?: SerializeOptions
}
```

2. **Prefer required properties** when a value should always be present. This reduces defensive coding and makes contract expectations clear:

```typescript
// Instead of allowing properties to be undefined and checking later
// Make them required in the interface/type definition
{
  status: edgeFunctionsStatus?.healthy,
  isSuccess: edgeFunctionsStatus?.healthy,
}
```

3. **Add explicit null checks** before accessing properties of potentially undefined objects:

```typescript
// Bad - may cause errors if currentOrg is undefined
enabled: !['team', 'enterprise'].includes(currentOrg?.plan.id ?? ''),

// Good - explicitly check existence first
enabled: currentOrg !== undefined && !['team', 'enterprise'].includes(currentOrg?.plan.id ?? ''),
```

Consistently applying these practices helps prevent null reference errors and makes code behavior more predictable across the codebase.