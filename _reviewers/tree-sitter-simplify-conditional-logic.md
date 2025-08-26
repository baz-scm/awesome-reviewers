---
title: Simplify conditional logic
description: Improve code readability by simplifying complex conditional expressions
  and control flow structures. Factor out repeated boolean expressions from nested
  conditions, use early returns instead of result variables when possible, and consolidate
  related conditional blocks.
repository: tree-sitter/tree-sitter
label: Code Style
language: C
comments_count: 4
repository_stars: 21799
---

Improve code readability by simplifying complex conditional expressions and control flow structures. Factor out repeated boolean expressions from nested conditions, use early returns instead of result variables when possible, and consolidate related conditional blocks.

Key practices:
- Extract common boolean expressions to reduce duplication and improve clarity
- Prefer early returns over result variables to reduce nesting and make control flow more obvious  
- Combine related conditional checks into unified blocks rather than separate statements
- Structure conditional logic to minimize cognitive load

Example of factoring out boolean expressions:
```c
// Instead of:
if ((!is_empty && ts_node_end_byte(node) <= self->start_byte) ||
    (!is_empty && point_lte(ts_node_end_point(node), self->start_point)))

// Use:
if (!is_empty && (
    ts_node_end_byte(node) <= self->start_byte ||
    point_lte(ts_node_end_point(node), self->start_point)))
```

Example of consolidating conditionals:
```c
// Instead of separate error checks:
if (e == PARENT_DONE) {
  cleanup();
  return TSQueryErrorSyntax;
}
if (e) {
  cleanup();
  return e;
}

// Use unified approach:
if (e) {
  cleanup();
  if (e == PARENT_DONE) e = TSQueryErrorSyntax;
  return e;
}
```