---
title: Graceful error recovery
description: Implement error handling that accumulates diagnostics rather than failing
  immediately, especially for operations that could help users identify and fix problems.
  Design systems to continue functioning when possible, with configurable strictness
  levels.
repository: vercel/turborepo
label: Error Handling
language: Other
comments_count: 2
repository_stars: 28115
---

Implement error handling that accumulates diagnostics rather than failing immediately, especially for operations that could help users identify and fix problems. Design systems to continue functioning when possible, with configurable strictness levels.

For diagnostic operations like queries or validation, prioritize providing useful information even when errors exist. This helps users understand and fix issues rather than blocking them entirely.

Example implementation pattern:
```go
// Instead of immediately failing on first error
if err != nil {
  return fmt.Errorf("invalid task configuration: %w", err)
}

// Use a diagnostic collector approach
diagnostics := &DiagnosticCollector{}
if err != nil {
  diagnostics.Add(Diagnostic{
    Severity: Error,
    Message: fmt.Sprintf("invalid task configuration: %s", err),
  })
}

// Only fail immediately for critical errors or in execution mode
if !queryMode && diagnostics.HasErrors() {
  return diagnostics.Error()
}

// Otherwise, continue with as much functionality as possible
// but include warnings about the issues
return result, diagnostics.Warnings()
```

Consider providing configuration options for users to control error behavior, such as the `--continue` flag with values like "none", "independent-tasks-only", or "all" to specify which operations should continue when errors occur.