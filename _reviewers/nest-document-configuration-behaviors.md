---
title: Document configuration behaviors
description: 'Always document configuration options thoroughly, especially for module
  and service settings. For each configuration property:


  1. Provide clear descriptions of what the option does'
repository: nestjs/nest
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 71766
---

Always document configuration options thoroughly, especially for module and service settings. For each configuration property:

1. Provide clear descriptions of what the option does
2. Specify default values using the `@default` JSDoc tag when appropriate
3. Document different behaviors in different contexts (e.g., client vs server)
4. Add examples for complex configuration scenarios

This prevents developers from spending hours debugging unexpected behaviors. When default values differ between contexts or cannot use `@default` tags, explicitly explain the behavior in comments.

```typescript
export interface CacheModuleOptions extends CacheManagerOptions {
  /**
   * If "true', register `CacheModule` as a global module.
   * Note: This applies only at the top level CacheModuleAsyncOptions.isGlobal,
   * and will be ignored in useFactory return values.
   * @default false
   */
  isGlobal?: boolean;
}
```

For optional features or configurations that aren't enabled by default in examples, consider adding commented code with explanatory notes:

```typescript
// Uncomment these lines to enable Redis adapter
// const redisIoAdapter = new RedisIoAdapter(app);
// await redisIoAdapter.connectToRedis();
// app.useWebSocketAdapter(redisIoAdapter);
```

This approach significantly improves developer experience by preventing confusion and reducing time spent debugging configuration-related issues.