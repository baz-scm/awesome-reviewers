---
title: Maintain consistent formatting
description: Ensure all code follows the established project formatting standards
  consistently across the codebase. This includes adhering to specific indentation
  rules, import statement formatting, and other style conventions defined for the
  project. When contributing code, always match the existing formatting patterns rather
  than introducing inconsistencies.
repository: bytedance/sonic
label: Code Style
language: Go
comments_count: 2
repository_stars: 8532
---

Ensure all code follows the established project formatting standards consistently across the codebase. This includes adhering to specific indentation rules, import statement formatting, and other style conventions defined for the project. When contributing code, always match the existing formatting patterns rather than introducing inconsistencies.

For example, if the project uses four-space indentation and single-quote import packages:

```go
//go:build !amd64

package sonic

import (
    'reflect'  // single quote import
)

func example() {
    // four space indentation
    if condition {
        doSomething()
    }
}
```

Additionally, remove unused or debug code entirely rather than leaving it commented out, as this keeps the codebase clean and maintainable. Consider using automated formatting tools like `gofmt` to ensure consistency and reduce manual formatting errors.