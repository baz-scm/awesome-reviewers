---
title: Use conventional descriptive names
description: Variable names should follow established language conventions and clearly
  communicate their purpose and context. Avoid abbreviated or cryptic names in favor
  of descriptive identifiers that make code self-documenting.
repository: golang/go
label: Naming Conventions
language: Go
comments_count: 2
repository_stars: 129599
---

Variable names should follow established language conventions and clearly communicate their purpose and context. Avoid abbreviated or cryptic names in favor of descriptive identifiers that make code self-documenting.

Key principles:
- Follow language-specific naming conventions (e.g., use `err` instead of `e` for errors in Go)
- Choose names that reflect the variable's role and context (e.g., `writeSocket` instead of `parent-reads`)
- Prioritize clarity over brevity, especially in examples and documentation

Example of improvement:
```go
// Poor naming
r, e := http.Post("http://127.0.0.1/count", "text/plain", strings.NewReader("POST data"))
writeFile := os.NewFile(uintptr(fds[0]), "parent-reads")

// Better naming  
req, err := http.Post("http://127.0.0.1/count", "text/plain", strings.NewReader("POST data"))
writeSocket := os.NewFile(uintptr(fds[0]), "write-socket")
```

This approach improves code readability, reduces cognitive load for other developers, and aligns with community standards and expectations.