---
title: self-documenting code practices
description: Write code that explains itself through clear structure and meaningful
  names, while adding targeted comments only where necessary for future maintainability.
  Extract complex logic into well-named functions with comprehensive documentation,
  but avoid redundant comments that duplicate what the code already expresses clearly.
repository: apache/spark
label: Documentation
language: Other
comments_count: 4
repository_stars: 41554
---

Write code that explains itself through clear structure and meaningful names, while adding targeted comments only where necessary for future maintainability. Extract complex logic into well-named functions with comprehensive documentation, but avoid redundant comments that duplicate what the code already expresses clearly.

Key principles:
- Extract complex logic into dedicated functions with descriptive names and comprehensive documentation
- Add comments to explain non-obvious business logic or data structures for future readers
- Remove comments that simply restate what the code does - let clear exception messages and function names speak for themselves
- Organize code into logical groupings that make the overall structure self-evident

Example of good practice:
```scala
// Good: Extract complex logic with clear documentation
/**
 * Creates table filters for dataflow operations.
 * Maps expected filter results depending on combination of full refresh and partial refresh.
 */
private def createTableFilters(fullRefresh: Boolean, partialRefresh: Boolean): TableFilters = {
  // Implementation here
}

// Good: Targeted comment for future maintainers
// Providers that couldn't be processed now and need to be added back to the queue
val providersToRequeue = new ArrayBuffer[(StateStoreProviderId, StateStoreProvider)]()

// Avoid: Redundant comment that restates the obvious
// throw exception if pipeline does not have table or persisted view
throw new IllegalStateException("Pipeline must have table or persisted view")
```

This approach reduces maintenance burden by preventing stale comments while ensuring complex logic remains understandable to future developers.