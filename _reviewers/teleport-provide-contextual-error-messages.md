---
title: Provide contextual error messages
description: Error messages should be specific, contextual, and use appropriate error
  creation functions to help users understand what went wrong and how to fix it.
repository: gravitational/teleport
label: Error Handling
language: Go
comments_count: 3
repository_stars: 19109
---

Error messages should be specific, contextual, and use appropriate error creation functions to help users understand what went wrong and how to fix it.

**Key principles:**

1. **Include relevant context**: Error messages should contain specific identifiers, values, or context that help identify the source of the problem.

2. **Use appropriate error creation functions**: 
   - Use `errors.New()` for static error messages without formatting
   - Use `fmt.Errorf()` only when you need to include dynamic values
   - Use trace-specific functions like `trace.BadParameter()` when appropriate

3. **Be specific about the problem**: Avoid generic messages that don't help users understand what went wrong.

**Examples:**

```go
// Bad: Generic error without context
return trace.BadParameter("target is not an IC plugin")

// Good: Specific error with context
return trace.BadParameter("%q is not an AWS Identity Center integration", p.edit.awsIC.pluginName)

// Bad: Using fmt.Errorf for static messages
return fmt.Errorf("end time before start time")

// Good: Using errors.New for static messages
return errors.New("end time before start time")

// Good: Using fmt.Errorf when formatting is needed
return fmt.Errorf("invalid request size: expected %d bytes, got %d bytes", requestHeaderSize, len(data))
```

This approach improves debugging experience by providing actionable information that helps users identify and resolve issues quickly.