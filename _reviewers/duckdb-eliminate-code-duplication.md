---
title: Eliminate code duplication
description: 'Actively identify and eliminate code duplication to improve maintainability
  and reduce the risk of inconsistent behavior. This includes several strategies:'
repository: duckdb/duckdb
label: Code Style
language: C++
comments_count: 9
repository_stars: 32061
---

Actively identify and eliminate code duplication to improve maintainability and reduce the risk of inconsistent behavior. This includes several strategies:

**Reuse existing utilities instead of reimplementing:**
```cpp
// Instead of writing custom switch-case:
switch (expr->GetExpressionClass()) {
    case ExpressionClass::BOUND_COLUMN_REF:
        // handle case
        break;
    // ... more cases
}

// Use existing utility:
ExpressionIterator::EnumerateChildren(expr, [&](Expression &child) {
    // handle child
});
```

**Extract common functionality into shared methods:**
```cpp
// Instead of copy-pasted functions:
string FileHandle::ReadLine() {
    // duplicate implementation
}
string FileHandle::ReadLine(QueryContext context) {
    // same implementation with context
}

// Extract common logic:
string FileHandle::ReadLine() {
    return ReadLine(QueryContext());
}
```

**Use offset variables instead of duplicating code blocks:**
```cpp
// Instead of duplicating based on boolean flags:
if (!lhs_first) {
    for (idx_t i = 0; i < right_projection_map.size(); i++) {
        // code block A
    }
    for (idx_t i = 0; i < left_projection_map.size(); i++) {
        // code block B  
    }
} else {
    for (idx_t i = 0; i < left_projection_map.size(); i++) {
        // code block B (duplicate)
    }
    for (idx_t i = 0; i < right_projection_map.size(); i++) {
        // code block A (duplicate)
    }
}

// Use offset approach:
idx_t left_offset = lhs_first ? 0 : right_projection_map.size();
idx_t right_offset = lhs_first ? left_projection_map.size() : 0;
// Single implementation using offsets
```

**Create dedicated classes for repeated patterns:**
When the same pattern appears across multiple locations, extract it into a reusable class or struct. This is especially important for complex initialization patterns, common data structures, or frequently used utility functions.

Always check if existing utilities can accomplish the same goal before implementing new functionality.