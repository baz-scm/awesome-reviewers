---
title: go:build directive syntax
description: Ensure go:build directives follow correct syntax with no space between
  "//" and "go", and use proper logical operators for multiple conditions. Incorrect
  spacing causes the directive to be ignored by the compiler, potentially including
  wrong code for target environments.
repository: golang/go
label: Configurations
language: Go
comments_count: 2
repository_stars: 129599
---

Ensure go:build directives follow correct syntax with no space between "//" and "go", and use proper logical operators for multiple conditions. Incorrect spacing causes the directive to be ignored by the compiler, potentially including wrong code for target environments.

For multiple platforms, use OR operators (||) between conditions:
```go
//go:build aix || darwin || dragonfly || freebsd || netbsd || openbsd || solaris
```

For complex conditions, use parentheses and logical operators:
```go
//go:build (js && wasm) || windows
```

Common mistakes include adding spaces ("// go:build") or using comma-separated lists without operators. Always verify build constraints are properly recognized by checking compilation behavior across target platforms.