---
title: API documentation accuracy
description: Ensure API documentation examples use types, interfaces, and imports
  that actually exist in the documented versions. Verify that code examples can be
  successfully imported and executed before publishing documentation.
repository: nrwl/nx
label: API
language: Other
comments_count: 2
repository_stars: 27518
---

Ensure API documentation examples use types, interfaces, and imports that actually exist in the documented versions. Verify that code examples can be successfully imported and executed before publishing documentation.

When documenting API lifecycle information (deprecation timelines, future removals), validate these claims with maintainers rather than making assumptions. Avoid stating definitive future plans unless they are confirmed by the development team.

Example of problematic documentation:
```typescript
// Bad: Importing a type that doesn't exist in @nx/devkit@22+
import {
  CreateNodes,  // This type was removed!
  CreateNodesV2,
} from '@nx/devkit';
```

Example of corrected documentation:
```typescript
// Good: Only import types that exist in the target version
import {
  CreateNodesV2,
  CreateNodesContextV2,
} from '@nx/devkit';
```

Before documenting deprecation timelines, confirm with maintainers:
- "Nx 24: The createNodesV2 types will be removed" ← Verify this is actually planned
- Check if exports will truly be removed or just marked as deprecated

This prevents developers from following outdated or incorrect API guidance and ensures documentation remains a reliable reference.