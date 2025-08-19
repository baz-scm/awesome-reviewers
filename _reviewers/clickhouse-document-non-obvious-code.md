---
title: Document non-obvious code
description: Add explanatory comments for any code element that is not self-explanatory,
  including complex return types, method parameters, classes, and technical concepts
  that may not be familiar to all developers.
repository: ClickHouse/ClickHouse
label: Documentation
language: Other
comments_count: 7
repository_stars: 42425
---

Add explanatory comments for any code element that is not self-explanatory, including complex return types, method parameters, classes, and technical concepts that may not be familiar to all developers.

Key areas requiring documentation:
- **Complex return types**: Functions returning `std::pair` or other composite types should explain what each element represents
- **Method parameters**: Non-obvious parameters should have comments explaining their purpose and when they are used
- **Classes and structs**: All classes should have brief class-level comments explaining their purpose
- **Technical concepts**: Specialized implementations or domain-specific concepts should be explained for developers unfamiliar with the domain
- **Method names**: Methods with unclear names should have comments explaining their functionality

Examples:
```cpp
// Bad - no explanation of return values
std::pair<NamesAndTypesList, NamesAndTypesList> setupHivePartitioning(...);

// Good - clear explanation
/// Returns a pair of (partition_columns, regular_columns) extracted from the path
std::pair<NamesAndTypesList, NamesAndTypesList> setupHivePartitioning(...);

// Bad - no explanation of parameter
void prepareProcessedRequests(Coordination::Requests & requests, 
    LastProcessedFileInfoMapPtr created_nodes = nullptr);

// Good - parameter purpose explained
/// Prepare keeper requests, required to set file as Processed.
/// @param created_nodes - map of newly created nodes for tracking, passed when...
void prepareProcessedRequests(Coordination::Requests & requests,
    LastProcessedFileInfoMapPtr created_nodes = nullptr);

// Bad - no class documentation
struct HiveStylePartitionStrategy : PartitionStrategy

// Good - explains the concept
/// Implements Hive-style partitioning where data is organized into directories
/// based on partition key values (e.g., year=2023/month=01/data.parquet)
struct HiveStylePartitionStrategy : PartitionStrategy
```

The goal is to make code self-documenting and reduce the cognitive load for future maintainers who may not be familiar with the specific domain or implementation details.