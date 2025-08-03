---
title: Protect shared state access
description: 'Ensure thread-safe access to shared state by using appropriate synchronization
  mechanisms and atomic operations. Avoid race conditions by:


  1. Using atomic operations or locks when modifying shared state'
repository: RooCodeInc/Roo-Code
label: Concurrency
language: TypeScript
comments_count: 9
repository_stars: 17288
---

Ensure thread-safe access to shared state by using appropriate synchronization mechanisms and atomic operations. Avoid race conditions by:

1. Using atomic operations or locks when modifying shared state
2. Acquiring locks in a consistent order to prevent deadlocks
3. Ensuring state consistency during async operations
4. Properly handling cleanup of async resources

Example of unsafe code:
```typescript
class StateManager {
    private cachedInfo: ModelInfo | null = null;
    
    async getInfo() {
        if (!this.cachedInfo) {  // Race condition: multiple threads might pass this check
            this.cachedInfo = await fetchModelInfo();  // Multiple simultaneous fetches possible
        }
        return this.cachedInfo;
    }
}
```

Safe version:
```typescript
class StateManager {
    private cachedInfo: ModelInfo | null = null;
    private fetchPromise: Promise<ModelInfo> | null = null;
    
    async getInfo() {
        if (this.fetchPromise) {
            return this.fetchPromise;  // Reuse in-flight request
        }
        
        if (!this.cachedInfo) {
            this.fetchPromise = fetchModelInfo();
            try {
                this.cachedInfo = await this.fetchPromise;
            } finally {
                this.fetchPromise = null;  // Clear promise reference
            }
        }
        return this.cachedInfo;
    }
}
```

This pattern prevents multiple simultaneous fetches, handles errors gracefully, and maintains state consistency across async operations.