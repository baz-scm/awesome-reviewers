---
title: Extract shared code patterns
description: Identify and extract repeated code patterns into reusable functions to
  improve maintainability and reduce duplication. When similar code appears in multiple
  places, create a shared helper function that captures the common logic.
repository: vitessio/vitess
label: Code Style
language: Go
comments_count: 6
repository_stars: 19815
---

Identify and extract repeated code patterns into reusable functions to improve maintainability and reduce duplication. When similar code appears in multiple places, create a shared helper function that captures the common logic.

Key guidelines:
- Extract code that differs only in a few parameters
- Create well-named helper functions that clearly describe their purpose
- Pass varying elements as parameters
- Consider creating dedicated types for related helpers

Example - Before:
```go
func (tc *TransitiveClosures) Add(exprA, exprB sqlparser.Expr, comp string) {
    // Duplicate logic for handling expressions
    if tc.setA.contains(exprA) {
        // Complex logic A
    }
    if tc.setB.contains(exprB) {
        // Complex logic A repeated
    }
}
```

After:
```go
func (tc *TransitiveClosures) handleExpr(expr sqlparser.Expr, set *exprSet) {
    // Shared logic extracted
    if set.contains(expr) {
        // Complex logic in one place
    }
}

func (tc *TransitiveClosures) Add(exprA, exprB sqlparser.Expr, comp string) {
    tc.handleExpr(exprA, tc.setA)
    tc.handleExpr(exprB, tc.setB)
}
```

This pattern reduces maintenance burden, improves readability, and makes the code easier to modify since changes only need to be made in one place.