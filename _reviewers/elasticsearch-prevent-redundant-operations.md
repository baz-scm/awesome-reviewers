---
title: Prevent redundant operations
description: 'In distributed database systems, prevent redundant operations that can
  overload cluster resources. When implementing update operations that might be triggered
  simultaneously from multiple nodes:'
repository: elastic/elasticsearch
label: Database
language: Java
comments_count: 5
repository_stars: 73104
---

In distributed database systems, prevent redundant operations that can overload cluster resources. When implementing update operations that might be triggered simultaneously from multiple nodes:

1. Add conditional checks to avoid redundant processing when the state hasn't changed:

```java
// Before applying mapping updates, check if they're identical to existing mappings
if (existingMapper != null && sourceToMerge.equals(existingMapper.mappingSource())) {
    context.resetForNoopMappingUpdateRetry(initialMappingVersion);
    return true;
}
```

2. Consider sequencing operations when high concurrency is expected, especially for resource-intensive updates:
   - Execute updates sequentially rather than allowing parallel execution
   - For critical operations, consider coordinating through a single node (like the master node)
   - Use appropriate locking or versioning mechanisms to prevent conflicting updates

3. Use direct access methods to avoid constructing unnecessary intermediate objects:
   - Access metadata directly with methods like `getProjectMetadata()` instead of constructing full state objects
   - Preserve important properties like query boost and name parameters when transforming queries

These optimizations are particularly important when multiple data nodes might be issuing similar updates (like dynamic mappings) or when working near capacity limits of the system.
