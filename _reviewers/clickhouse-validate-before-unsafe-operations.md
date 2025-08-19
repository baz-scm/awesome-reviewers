---
title: Validate before unsafe operations
description: Always validate values before performing operations that could result
  in undefined behavior, particularly dynamic casts and arithmetic on unsigned types
  that might underflow.
repository: ClickHouse/ClickHouse
label: Null Handling
language: C++
comments_count: 3
repository_stars: 42425
---

Always validate values before performing operations that could result in undefined behavior, particularly dynamic casts and arithmetic on unsigned types that might underflow.

For dynamic_cast operations, check the result for nullptr before use, even if you expect the cast to succeed:

```cpp
DatabaseReplicated * replicated_database = dynamic_cast<DatabaseReplicated *>(database.get());
if (!replicated_database) {
    throw Exception(ErrorCodes::LOGICAL_ERROR, "Expected replicated database");
}
```

For unsigned arithmetic that could underflow, validate inputs first:

```cpp
// Before: UInt8 event_idx = event_type - 1;  // Underflows if event_type == 0
// After:
if (event_type == 0) {
    // Handle the no-match case appropriately
    continue;
}
UInt8 event_idx = event_type - 1;
```

This defensive approach prevents crashes and undefined behavior that can be difficult to debug, especially when the problematic values come from external data or user input. The small performance cost of validation is typically worthwhile compared to the cost of debugging production crashes.