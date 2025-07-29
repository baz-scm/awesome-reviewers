---
title: API consistency patterns
description: 'Ensure API design follows consistent patterns for naming, typing, and
  composition to improve developer experience and maintainability.


  **Key principles:**'
repository: remix-run/react-router
label: API
language: TypeScript
comments_count: 12
repository_stars: 55270
---

Ensure API design follows consistent patterns for naming, typing, and composition to improve developer experience and maintainability.

**Key principles:**

1. **Use fully qualified names in deprecation messages** - Include the full path like `MetaArgs.loaderData` instead of just `loaderData` to provide clear migration guidance.

2. **Prefer type-only imports for types** - Use `import type { ServerBuild }` instead of `import { ServerBuild }` when importing only for type annotations.

3. **Use consistent generic parameter naming** - Prefer descriptive names like `Context` over abbreviated forms like `C` for better readability:
```typescript
export interface LoaderFunction<Context = any> {
  (args: LoaderFunctionArgs<Context>): Promise<DataFunctionValue> | DataFunctionValue;
}
```

4. **Choose appropriate type definitions** - Use `export type` for simple function signatures instead of interfaces when no extension is needed:
```typescript
export type HeadersFunction = (args: HeadersArgs) => Headers | HeadersInit;
```

5. **Build composable APIs** - Design new functions to leverage existing ones rather than duplicating logic:
```typescript
export const redirectWithReload: RedirectFunction = (url, init) => {
  let response = redirect(url, init);
  response.headers.set("X-Remix-Reload-Document", "true");
  return response;
};
```

6. **Preserve request context appropriately** - When creating new request objects, copy relevant properties from the original rather than creating minimal requests:
```typescript
let loaderRequest = new Request(request.url, {
  body: null,
  headers: request.headers,
  method: request.method,
  redirect: request.redirect,
  signal: request.signal,
});
```

These patterns improve API discoverability, reduce confusion during migrations, and create more predictable interfaces for developers.