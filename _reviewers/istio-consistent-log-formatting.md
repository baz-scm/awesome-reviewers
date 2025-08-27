---
title: consistent log formatting
description: Maintain consistent formatting conventions across log messages to improve
  code readability and debugging effectiveness. Use proper format specifiers (%v for
  errors, not %s), maintain consistent spacing around punctuation (no spaces before
  colons), and ensure consistent label semantics when logging similar data structures.
repository: istio/istio
label: Logging
language: Go
comments_count: 3
repository_stars: 37192
---

Maintain consistent formatting conventions across log messages to improve code readability and debugging effectiveness. Use proper format specifiers (%v for errors, not %s), maintain consistent spacing around punctuation (no spaces before colons), and ensure consistent label semantics when logging similar data structures.

Key formatting guidelines:
- Use `%v` format specifier for error values instead of `%s`
- Avoid spaces before colons in messages: "error: %v" not "error : %v"  
- Keep error messages concise by avoiding redundant phrases like "with error"
- Use consistent label names and value types for similar data across different log statements

Example of good formatting:
```go
// Good - consistent formatting, proper specifier
log.Infof("connection closed: %v", err)
log.WithLabels("removes", len(resp.RemovedResources)).Debugf("forward ECDS")

// Bad - inconsistent spacing, wrong specifier, redundant text
log.Infof("connection is not closed with error : %s", err)  
log.WithLabels("removals", resp.RemovedResources).Debugf("forward ECDS")
```

This consistency helps maintain professional code quality and makes log analysis more predictable for debugging and monitoring.