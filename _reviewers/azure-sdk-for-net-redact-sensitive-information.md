---
title: Redact sensitive information
description: Always sanitize configuration data or any potentially sensitive information
  before logging or displaying it. When logging configurations, API responses, or
  user inputs, use pattern matching to identify and redact secrets, passwords, API
  keys, and other credentials.
repository: Azure/azure-sdk-for-net
label: Security
language: Other
comments_count: 1
repository_stars: 5809
---

Always sanitize configuration data or any potentially sensitive information before logging or displaying it. When logging configurations, API responses, or user inputs, use pattern matching to identify and redact secrets, passwords, API keys, and other credentials.

Example implementation:
```powershell
# WRONG: Directly logging raw configuration
Write-Host $rawConfig

# CORRECT: Redacting sensitive information before logging
$safeConfig = $rawConfig -replace '(?i)(\"(password|secret|key)\":\s*\".*?\")', '"$1":"[REDACTED]"'
Write-Host $safeConfig
```

This pattern prevents accidental exposure of sensitive information in logs, console output, or error messages that might be viewed by unauthorized personnel or stored in insecure locations. Implement similar redaction mechanisms in all logging and output systems across your codebase.
