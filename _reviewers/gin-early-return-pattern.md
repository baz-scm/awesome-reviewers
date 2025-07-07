---
title: Early return pattern
description: Prefer returning early from functions rather than nesting conditions.
  When a condition can lead to an early exit, handle it immediately and return rather
  than wrapping the main logic in else blocks. This approach reduces nesting, improves
  code readability, and reduces cognitive load.
repository: gin-gonic/gin
label: Code Style
language: Go
comments_count: 3
repository_stars: 83022
---

Prefer returning early from functions rather than nesting conditions. When a condition can lead to an early exit, handle it immediately and return rather than wrapping the main logic in else blocks. This approach reduces nesting, improves code readability, and reduces cognitive load.

**Instead of this:**
```go
func debugPrint(format string, values ...interface{}) {
  if IsDebugging() {
    if DebugPrintFunc == nil {
      if !strings.HasSuffix(format, "\n") {
        format += "\n"
      }
      fmt.Fprintf(DefaultWriter, "[GIN-debug] "+format, values...)
    } else {
      DebugPrintFunc(format, values...)
    }
  }
}
```

**Use this:**
```go
func debugPrint(format string, values ...interface{}) {
  if !IsDebugging() {
    return
  }

  if DebugPrintFunc != nil {
    DebugPrintFunc(format, values...)
    return
  }

  if !strings.HasSuffix(format, "\n") {
    format += "\n"
  }
  fmt.Fprintf(DefaultWriter, "[GIN-debug] "+format, values...)
}
```

The early return pattern simplifies the code flow, making it easier to understand at a glance. It also helps prevent the "arrow code" or "pyramid of doom" where multiple nested conditions create deeply indented code blocks.