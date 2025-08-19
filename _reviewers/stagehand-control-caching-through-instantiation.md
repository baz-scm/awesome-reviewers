---
title: Control caching through instantiation
description: When implementing optional caching functionality, control cache behavior
  through conditional instantiation at higher abstraction levels rather than adding
  conditional logic within cache implementations themselves. This approach maintains
  cleaner separation of concerns and avoids scattered conditional checks throughout
  cache methods.
repository: browserbase/stagehand
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 16443
---

When implementing optional caching functionality, control cache behavior through conditional instantiation at higher abstraction levels rather than adding conditional logic within cache implementations themselves. This approach maintains cleaner separation of concerns and avoids scattered conditional checks throughout cache methods.

Instead of adding enableCaching flags and conditional logic within cache classes:

```typescript
// Avoid this pattern
export class BaseCache<T extends CacheEntry> {
  protected enableCaching: boolean;
  
  protected ensureCacheDirectory(): void {
    if (this.enableCaching && !fs.existsSync(this.cacheDir)) {
      fs.mkdirSync(this.cacheDir, { recursive: true });
    }
  }
}
```

Prefer conditional instantiation at the consumer level:

```typescript
// Prefer this pattern
class LLMProvider {
  private cache?: BaseCache<LLMCacheEntry>;
  
  constructor(enableCaching: boolean) {
    this.cache = enableCaching ? new BaseCache() : undefined;
  }
  
  private async makeCall() {
    if (this.cache) {
      // Use cache operations
    }
  }
}
```

This pattern keeps cache implementations focused on their core responsibility while allowing higher-level components to control when caching is active.