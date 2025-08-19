---
title: validate inputs early
description: Validate function inputs, preconditions, and assumptions as early as
  possible in the execution flow, preferably during binding or initialization phases
  rather than deep within implementation logic. This prevents invalid states from
  propagating through the system and ensures errors are caught at the appropriate
  architectural level.
repository: duckdb/duckdb
label: Error Handling
language: C++
comments_count: 5
repository_stars: 32061
---

Validate function inputs, preconditions, and assumptions as early as possible in the execution flow, preferably during binding or initialization phases rather than deep within implementation logic. This prevents invalid states from propagating through the system and ensures errors are caught at the appropriate architectural level.

Early validation should check for:
- Input parameter validity and type correctness
- Preconditions that must be met before processing
- Resource availability and state consistency
- Duplicate or conflicting arguments

Example of good early validation:
```cpp
// In bind phase - catch errors before execution starts
static unique_ptr<FunctionData> ListContainsBind(ClientContext &context, ScalarFunction &bound_function,
                                                vector<unique_ptr<Expression>> &arguments) {
    // Check for unsupported nested types early
    if (arguments[1]->return_type.id() == LogicalTypeId::LIST) {
        throw NotImplementedException("This function has not yet been implemented for nested types");
    }
    // Validate map type assumption before using it
    if (map_logical_type.id() != LogicalTypeId::MAP) {
        throw InvalidInputException("Expected MAP type, got %s", map_logical_type.ToString());
    }
}
```

Example of problematic late validation:
```cpp
// Bad - validating deep in execution logic
static void SomeFunction(DataChunk &args, ExpressionState &state, Vector &result) {
    // ... lots of processing ...
    if (children.size() != 1) {  // Should be caught much earlier
        throw InvalidInputException("Expected single child");
    }
}
```

This approach reduces debugging complexity, provides clearer error messages with better context, and prevents resource waste on operations that are destined to fail.