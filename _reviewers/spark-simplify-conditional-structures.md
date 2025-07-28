---
title: Simplify conditional structures
description: Organize complex conditional logic using clear, sequential patterns rather
  than nested structures or multiple early returns. This improves code readability
  and maintainability by making the flow of logic easier to follow.
repository: apache/spark
label: Code Style
language: Other
comments_count: 7
repository_stars: 41554
---

Organize complex conditional logic using clear, sequential patterns rather than nested structures or multiple early returns. This improves code readability and maintainability by making the flow of logic easier to follow.

Key practices:
- **Avoid nested conditionals**: Use consecutive checks instead of deeply nested if-else structures
- **Organize exit points early**: Move validation checks and early returns to the beginning of methods
- **Use match statements for complex combinations**: When dealing with multiple related conditions, prefer pattern matching over sequential if-else chains
- **Eliminate early returns in loops**: Structure conditional flow to return a single value at the end

Example of improvement:
```scala
// Instead of nested conditionals:
windowExpression.windowFunction match {
  case AggregateExpression(_, _, true, _, _) =>
    // nested validation logic
}

// Use consecutive checks with extracted methods:
checkWindowFunction(windowExpression)
checkWindowFunctionAndFrameMismatch(windowExpression)
```

For complex parameter combinations, prefer explicit pattern matching:
```scala
// Instead of sequential validation:
if (fullRefreshTables.nonEmpty && fullRefreshAll) { ... }
if (refreshTables.nonEmpty && fullRefreshAll) { ... }

// Use pattern matching:
(fullRefreshTables, refreshTableNames) match {
  case (Nil, Nil) => ...
  case (fullRefreshTables, Nil) => ...
  case ...
}
```

This approach reduces cognitive load and makes the code's intent clearer by explicitly handling each logical case.