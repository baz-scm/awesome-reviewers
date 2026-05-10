---
title: Enforce shared code style
description: 'Keep style consistent by following the team’s codified rules for both
  formatting and language idioms, and enforce them via shared tooling.


  Apply this as a checklist:'
repository: kamranahmedse/developer-roadmap
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 354523
---

Keep style consistent by following the team’s codified rules for both formatting and language idioms, and enforce them via shared tooling.

Apply this as a checklist:
- Use the team’s shared style configuration (e.g., a `stylecop.json` checked into the repo) so formatting rules are the same for everyone and across IDEs.
- Respect whitespace/structure rules consistently (for example, maintain required blank lines around headings/sections in docs).
- Follow language-specific style/idiom constraints, not just “compiles”: e.g., in Go prefer `:=` only where it’s valid.

Go example (idioms):
```go
// Package/global: prefer var
var x int // zero value

func f() {
    y := 1          // ok: inside function
    if z := y + 1; true {
        _ = z       // ok: temp in if init
    }

    // Redeclare semantics: one variable must be new
    a, b := 1, 2
    a, b = 3, 4 // plain assignment
    a, c := 5, 6 // redeclare with := where one LHS name is new
}
```