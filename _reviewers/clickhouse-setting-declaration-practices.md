---
title: Setting declaration practices
description: Always declare settings before using them and optimize access patterns
  for performance. Settings must be properly declared in the appropriate scope before
  being referenced in code. When accessing settings multiple times, cache the value
  in a local variable to avoid repeated lookups. For configuration parsing, avoid
  modifying AST nodes directly and use local...
repository: ClickHouse/ClickHouse
label: Configurations
language: C++
comments_count: 4
repository_stars: 42425
---

Always declare settings before using them and optimize access patterns for performance. Settings must be properly declared in the appropriate scope before being referenced in code. When accessing settings multiple times, cache the value in a local variable to avoid repeated lookups. For configuration parsing, avoid modifying AST nodes directly and use local variables instead.

Example of proper setting declaration and usage:
```cpp
// Declare setting before use
DECLARE(UInt64, database_replicated_logs_to_keep, 1000, "Description", 0)

// Cache setting value when used multiple times
bool enable_optimization = planner_context->getQueryContext()->getSettingsRef()[Setting::enable_add_distinct_to_in_subqueries];
for (const auto & item : items) {
    if (enable_optimization) {
        // Use cached value instead of repeated setting access
    }
}

// Avoid modifying AST, use local variables
auto key_value = evaluateConstantExpressionOrIdentifierAsLiteral(children[0], context);
// Store in local variable instead of updating children[0] directly
```

This practice prevents runtime errors from undeclared settings, improves performance by reducing repeated setting lookups, and maintains cleaner code by avoiding direct AST modifications during configuration parsing.