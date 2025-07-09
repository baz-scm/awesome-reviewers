---
title: Balance flexibility with performance
description: When designing APIs, carefully balance flexibility against performance
  constraints. More flexible APIs often come with implementation complexity and potential
  performance costs. Start by understanding how clients actually use your API, then
  optimize for those common patterns while providing just enough flexibility for legitimate
  edge cases.
repository: neondatabase/neon
label: API
language: Other
comments_count: 2
repository_stars: 19015
---

When designing APIs, carefully balance flexibility against performance constraints. More flexible APIs often come with implementation complexity and potential performance costs. Start by understanding how clients actually use your API, then optimize for those common patterns while providing just enough flexibility for legitimate edge cases.

For example, in an RPC service for batch operations, consider whether clients typically need scattered or contiguous page requests:

```protobuf
// More flexible but potentially less optimized approach
message GetPageRequestBatch {
  repeated GetPageRequest requests = 1;  // Allows arbitrary pages
}

// More constrained but potentially more optimized approach
message GetContiguousPageRequest {
  uint64 request_id = 1;
  GetPageClass request_class = 2;
  ReadLsn read_lsn = 3;
  RelTag rel = 4;
  uint32 start_block_number = 5;
  uint32 block_count = 6;  // Enforces contiguous ranges
}
```

When evaluating API design decisions, ask: "Is this flexibility actually needed by clients?" As one reviewer noted: "Since the batching exists for performance, I think it's best to limit the freedom. It might allow skipping some overhead." At the same time, consider consistent patterns across similar endpoints to make your API more intuitive and maintainable.