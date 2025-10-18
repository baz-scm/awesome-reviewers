---
title: reuse existing code
description: Before implementing new functionality, check if similar utilities or
  patterns already exist in the codebase. Consolidate duplicate logic and leverage
  existing libraries to maintain consistency and reduce maintenance overhead.
repository: sst/opencode
label: Code Style
language: Go
comments_count: 3
repository_stars: 28213
---

Before implementing new functionality, check if similar utilities or patterns already exist in the codebase. Consolidate duplicate logic and leverage existing libraries to maintain consistency and reduce maintenance overhead.

Key practices:
- Search the codebase for existing utilities before creating new ones (e.g., use existing `ansi.Strip` instead of implementing `util.StripAnsi`)
- Combine similar functionality rather than creating separate handlers (e.g., add `ctrl+p` to existing `Up` binding instead of creating separate `CtrlP` binding)
- Move expensive operations to appropriate lifecycle methods to avoid repeated execution in frequently called functions

Example:
```go
// Instead of creating new utility
out := util.StripAnsi(fmt.Sprintf("%s", stdout))

// Reuse existing library
out := ansi.Strip(fmt.Sprintf("%s", stdout))
```

This approach improves code maintainability, reduces duplication, and ensures consistent patterns across the codebase.