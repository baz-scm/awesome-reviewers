---
title: Use configuration service injection
description: Replace mutable singletons and getter functions with dependency injection
  services for configuration-dependent components. This approach eliminates race conditions,
  provides proper initialization guarantees, and enables environment-specific configuration
  management.
repository: unionlabs/union
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 74800
---

Replace mutable singletons and getter functions with dependency injection services for configuration-dependent components. This approach eliminates race conditions, provides proper initialization guarantees, and enables environment-specific configuration management.

Instead of using mutable globals or getter functions:
```typescript
let client: ReturnType<typeof createClient<Database>> | null = null

export const getSupabaseClient = () =>
  Effect.gen(function*() {
    if (client) {
      return client
    }
    // initialization logic...
    client = createClient<Database>(url, anonKey)
    return client
  })
```

Use Effect services with proper environment variable validation:
```typescript
export class SupabaseClient extends Effect.Service<SupabaseClient>()("SupabaseClient", {
  scoped: (options?: SupabaseOptions | undefined) =>
    Effect.gen(function*() {
      const url = yield* S.decode(S.URL)(PUBLIC_SUPABASE_URL).pipe(
        Effect.mapError((cause) =>
          new SupabaseClientError({
            operation: "init",
            message: "Could not decode PUBLIC_SUPABASE_URL to URL",
            cause,
          })
        ),
      )
      const anonKey = yield* S.decode(S.NonEmptyString)(PUBLIC_SUPABASE_ANON_KEY).pipe(
        Effect.mapError((cause) =>
          new SupabaseClientError({
            operation: "init", 
            message: "Could not decode PUBLIC_SUPABASE_ANON_KEY to non-empty string",
            cause,
          })
        ),
      )
      return createClient<Database>(url.toString(), anonKey, options)
    }),
}) {}
```

This pattern ensures configuration is validated at startup, supports environment-specific layers (test vs production), and provides type-safe dependency injection throughout the application.