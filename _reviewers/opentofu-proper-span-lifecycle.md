---
title: Proper span lifecycle
description: Always ensure trace spans are properly closed in all code execution paths
  to prevent trace leaks that can distort observability data. This is particularly
  critical when creating spans within loops, conditional blocks, or functions with
  multiple exit points.
repository: opentofu/opentofu
label: Observability
language: Go
comments_count: 4
repository_stars: 25901
---

Always ensure trace spans are properly closed in all code execution paths to prevent trace leaks that can distort observability data. This is particularly critical when creating spans within loops, conditional blocks, or functions with multiple exit points.

When adding tracing to your code, follow these practices:

1. Use `defer span.End()` immediately after span creation when possible:
```go
ctx, span := tracing.Tracer().Start(ctx, "Operation")
defer span.End()
```

2. For spans in loops, either:
   - Extract loop body to a separate function where you can use defer
   - Explicitly end spans before continues/breaks/returns
   - Consider wrapping the loop body in a function literal with defer

3. Verify spans are ended in all execution paths, especially when error conditions cause early returns.

4. Be particularly careful with spans passed to callback functions to ensure they're properly closed.

Failure to close spans will cause them to remain open until timeout, potentially creating misleading timing data and resource leaks in your tracing backend.