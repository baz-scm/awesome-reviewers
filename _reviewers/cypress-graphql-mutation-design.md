---
title: GraphQL mutation design
description: Design GraphQL mutations to return meaningful objects rather than simple
  booleans, and use simple ID parameters instead of complex nested objects. This follows
  GraphQL best practices and enables proper client-side cache management.
repository: cypress-io/cypress
label: API
language: TypeScript
comments_count: 4
repository_stars: 48850
---

Design GraphQL mutations to return meaningful objects rather than simple booleans, and use simple ID parameters instead of complex nested objects. This follows GraphQL best practices and enables proper client-side cache management.

**Return Objects from Mutations:**
Mutations should return the modified entity to enable Apollo Client's normalized cache to update automatically. Returning just `true` or simple scalars requires manual cache updates.

```ts
// ❌ Avoid - returns boolean, requires manual cache updates
t.nonNull.field('addProject', {
  type: 'Boolean',
  async resolve(_root, args, ctx) {
    await ctx.projects.addProject(args)
    return true
  }
})

// ✅ Prefer - returns Project object for automatic cache updates
t.nonNull.field('addProject', {
  type: 'Project',
  async resolve(_root, args, ctx) {
    const project = await ctx.projects.addProject(args)
    return project
  }
})
```

**Use Simple ID Parameters:**
Prefer simple ID arguments over complex nested objects to keep the API clean and leverage server-side knowledge of entity relationships.

```ts
// ❌ Avoid - complex nested object parameter
t.nonNull.field('setCurrentSpec', {
  args: {
    spec: nonNull(inputObjectType({ /* complex spec object */ }))
  }
})

// ✅ Prefer - simple ID parameter
t.nonNull.field('setCurrentSpec', {
  args: {
    specId: nonNull(idArg())
  }
})
```

This approach reduces API complexity, improves type safety, and follows GraphQL conventions for client-server communication.