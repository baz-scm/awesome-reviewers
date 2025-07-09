---
title: Log levels and clarity
description: 'Choose appropriate log levels and write clear, meaningful log messages
  that provide necessary context without creating noise. Follow these guidelines:'
repository: vitessio/vitess
label: Logging
language: Go
comments_count: 4
repository_stars: 19815
---

Choose appropriate log levels and write clear, meaningful log messages that provide necessary context without creating noise. Follow these guidelines:

1. Use appropriate log levels:
   - ERROR: For issues requiring immediate attention
   - WARNING: For potentially problematic situations
   - INFO: For significant state changes or important operations
   - Avoid logging routine operations at INFO level

2. Include relevant context in messages:
   - Add identifiers (e.g., workflow names, IDs)
   - Explain the action being attempted, not just the result
   - Use structured formatting for complex objects (%+v)

Example of good logging:
```go
// Bad
log.Info("Operation failed")
log.Info("Starting operation")

// Good
log.Errorf("Failed to revert denied tables for workflow %v: %v", workflowName, err)
log.Infof("Starting VReplication player id: %v, settings: %+v", id, settings)
```

3. Avoid duplicate logging:
   - Don't log the same information at multiple levels
   - Choose the most appropriate single level for each message

4. Consider log readers:
   - Write messages that make sense without deep system knowledge
   - Include enough context to understand the operation's purpose