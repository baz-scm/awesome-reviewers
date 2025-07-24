---
title: Prevent information disclosure
description: Avoid exposing sensitive information through error messages, logs, configuration,
  or other output channels that might be accessible to unauthorized parties such as
  cluster administrators or operators.
repository: kubernetes/kubernetes
label: Security
language: Go
comments_count: 4
repository_stars: 116489
---

Avoid exposing sensitive information through error messages, logs, configuration, or other output channels that might be accessible to unauthorized parties such as cluster administrators or operators.

When handling sensitive data like credentials, environment variables, or configuration files, ensure that:

1. **Error messages exclude sensitive content**: Return generic error messages instead of including raw data that might contain secrets
2. **Log sensitive operations without exposing values**: Log the fact that an operation occurred without including the sensitive data itself
3. **Disable dangerous features in restricted contexts**: Prevent execution of arbitrary code or access to host resources that could lead to information disclosure

Example of secure error handling:
```go
// Instead of:
return "", fmt.Errorf("invalid environment variable format: %s", line)

// Use:
klog.Errorf("ParseEnv failed at line %d: %s", lineNum, line) // Log for debugging
return "", fmt.Errorf("invalid environment variable format at line %d", lineNum) // Safe error for user
```

This principle applies to environment variable parsing, credential management, configuration validation, and any feature that processes user-provided data that might contain secrets. Always consider who has access to error messages and logs before including potentially sensitive information.