---
title: Use appropriate log levels
description: Always match logging levels to the message's purpose and severity. Use
  log.Info for general information, log.Warn for warnings, and log.Error for error
  conditions. Avoid using fmt.Println for logging as it bypasses the logging framework's
  level-based filtering capabilities.
repository: kubeflow/kubeflow
label: Logging
language: Go
comments_count: 3
repository_stars: 15064
---

Always match logging levels to the message's purpose and severity. Use log.Info for general information, log.Warn for warnings, and log.Error for error conditions. Avoid using fmt.Println for logging as it bypasses the logging framework's level-based filtering capabilities.

Keep these guidelines in mind:
- Start log messages with lowercase letters for consistency
- Use the proper level that reflects the message's importance
- Provide descriptive content in error messages that explains what went wrong

Example of incorrect logging:
```go
// Incorrect usage
fmt.Println("Present working directory is: %v", cwd)
log.Info("WARNING: Notebook container is not found, so could not update State of Notebook CR")
```

Example of correct logging:
```go
// Correct usage
log.Info("setting up workload identity", "ClientId", azure.AzureIdentityClientId)
log.Error("could not find the notebook container", "notebook-name", instance.Name)
```

Following these practices helps with log filtering, improves troubleshooting, and creates a consistent logging experience throughout the codebase.
