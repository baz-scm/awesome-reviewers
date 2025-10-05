---
title: Environment-aware configuration management
description: Ensure configuration management accounts for different environments and
  maintains backward compatibility during migrations. This includes using safe access
  patterns for global objects, versioning configuration keys, and preserving environment-specific
  behavior.
repository: TanStack/router
label: Configurations
language: TSX
comments_count: 3
repository_stars: 11590
---

Ensure configuration management accounts for different environments and maintains backward compatibility during migrations. This includes using safe access patterns for global objects, versioning configuration keys, and preserving environment-specific behavior.

Key practices:
1. **Safe Global Access**: Use optional chaining when accessing global objects that may not exist in all environments
2. **Version Configuration Keys**: Include version identifiers in storage/configuration keys to prevent conflicts during major updates
3. **Environment-Specific Behavior**: Maintain different configuration behavior for production vs development environments
4. **Migration Strategy**: Use proxy exports to maintain backward compatibility when restructuring packages

Example from the discussions:
```javascript
// Safe global access with optional chaining
__html: `(${restoreScroll.toString()})(${JSON.stringify(storageKey)},${JSON.stringify(resolvedKey)});__TSR__?.cleanScripts?.()`

// Versioned configuration keys
export const storageKey = 'tsr-scroll-restoration-v1-3'

// Proxy exports for backward compatibility
export { TanStackRouterDevtoolsInProd as TanStackRouterDevtools } from '@tanstack/react-router-devtools'
```

This approach prevents runtime errors in different environments, avoids configuration conflicts during updates, and ensures smooth transitions during package migrations.