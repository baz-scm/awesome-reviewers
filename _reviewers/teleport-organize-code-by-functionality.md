---
title: Organize code by functionality
description: Structure code based on what it does rather than how it's implemented.
  Group related functionality together, extract reusable components, and place code
  in appropriate packages or files to improve maintainability and readability.
repository: gravitational/teleport
label: Code Style
language: Go
comments_count: 10
repository_stars: 19109
---

Structure code based on what it does rather than how it's implemented. Group related functionality together, extract reusable components, and place code in appropriate packages or files to improve maintainability and readability.

Key principles:
- **Package organization**: Move code to appropriate packages based on its purpose. Consider using internal packages for code not intended for external consumption
- **File organization**: Separate concerns by moving related functionality (like wire protocols, encoding/decoding) into dedicated files
- **Function extraction**: Break down large, complex functions into smaller, focused components. Extract nested functions that access multiple variables into separate methods when it improves readability
- **Avoid duplication**: Consolidate duplicate logic by having one implementation call another, or extract shared functionality into helper functions
- **Business logic separation**: Keep protocol-specific logic separate from generic handlers

Example of good organization:
```go
// Instead of having everything in one large function
func (s *recordingPlayback) streamEvents(ctx context.Context, req *fetchRequest, ...) {
    // 200+ lines of complex logic with nested processEvent function
}

// Extract for better readability
func (s *recordingPlayback) streamEvents(ctx context.Context, req *fetchRequest, ...) {
    // Main orchestration logic
    for event := range eventsChan {
        if !s.processEvent(event, req) {
            break
        }
    }
}

func (s *recordingPlayback) processEvent(evt apievents.AuditEvent, req *fetchRequest) bool {
    // Focused event processing logic
}
```

This approach makes code easier to understand, test, and maintain by creating clear boundaries between different responsibilities.