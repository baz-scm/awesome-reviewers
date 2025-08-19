---
title: Avoid unnecessary allocations
description: Minimize memory allocations, data copying, and expensive operations by
  implementing early exits, using move semantics, and choosing appropriate buffer
  management strategies.
repository: ClickHouse/ClickHouse
label: Performance Optimization
language: C++
comments_count: 11
repository_stars: 42425
---

Minimize memory allocations, data copying, and expensive operations by implementing early exits, using move semantics, and choosing appropriate buffer management strategies.

Key optimization strategies:
1. **Early exits**: Return immediately when the result is known to avoid processing remaining data
2. **Move semantics**: Use std::move() instead of copying large objects like buffers
3. **Proper buffer sizing**: Use count() instead of offset() for total bytes, and resize() instead of repeated emplace_back()
4. **Avoid expensive conversions**: Use direct data insertion instead of converting to intermediate types like Field
5. **Cache sizing**: Limit cache sizes to prevent memory bloat in long-running threads

Example of early exit optimization:
```cpp
// Instead of checking condition in loop
for (size_t row = 0; row < input_rows_count; ++row) {
    dst_data[row] = filter ? filter->find(value.data, value.size) : true;
}

// Return early when filter is not found
if (!filter) {
    auto dst = ColumnVector<UInt8>::create();
    dst->getData().resize_fill(input_rows_count, 1);
    return dst;
}
```

Example of avoiding unnecessary copying:
```cpp
// Instead of copying buffer before send
message_transport->send(PostgreSQLProtocol::Messaging::CopyOutData(std::move(result_buf)));

// Then explicitly reinitialize if needed
result_buf = {};
```

These optimizations are particularly important in performance-critical paths where small improvements can have significant cumulative impact.