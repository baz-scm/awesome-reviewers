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


[
  {
    "discussion_id": "2178653902",
    "pr_number": 50998,
    "pr_file": "eng/common/scripts/job-matrix/Create-JobMatrix.ps1",
    "created_at": "2025-07-01T22:33:14+00:00",
    "commented_code": ")\n\n. $PSScriptRoot/job-matrix-functions.ps1\n. $PSScriptRoot/../logging.ps1\n\nif (!(Test-Path $ConfigPath)) {\n    Write-Error \"ConfigPath '$ConfigPath' does not exist.\"\n    exit 1\n}\n$config = GetMatrixConfigFromFile (Get-Content $ConfigPath -Raw)\n$rawConfig = Get-Content $ConfigPath -Raw\n$config = GetMatrixConfigFromFile $rawConfig\n# Strip empty string filters in order to be able to use azure pipelines yaml join()\n$Filters = $Filters | Where-Object { $_ }\n\nLogGroupStart \"Matrix generation configuration\"\nWrite-Host \"Configuration File: $ConfigPath\"\nWrite-Host $rawConfig",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2178653902",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50998,
        "pr_file": "eng/common/scripts/job-matrix/Create-JobMatrix.ps1",
        "discussion_id": "2178653902",
        "commented_code": "@@ -21,15 +21,27 @@ param (\n )\n \n . $PSScriptRoot/job-matrix-functions.ps1\n+. $PSScriptRoot/../logging.ps1\n \n if (!(Test-Path $ConfigPath)) {\n     Write-Error \"ConfigPath '$ConfigPath' does not exist.\"\n     exit 1\n }\n-$config = GetMatrixConfigFromFile (Get-Content $ConfigPath -Raw)\n+$rawConfig = Get-Content $ConfigPath -Raw\n+$config = GetMatrixConfigFromFile $rawConfig\n # Strip empty string filters in order to be able to use azure pipelines yaml join()\n $Filters = $Filters | Where-Object { $_ }\n \n+LogGroupStart \"Matrix generation configuration\"\n+Write-Host \"Configuration File: $ConfigPath\"\n+Write-Host $rawConfig",
        "comment_created_at": "2025-07-01T22:33:14+00:00",
        "comment_author": "Copilot",
        "comment_body": "Printing the entire raw configuration may expose sensitive information; consider redacting secrets or limiting the amount of output.\n```suggestion\n$safeConfig = $rawConfig -replace '(?i)(\\\"(password|secret|key)\\\":\\s*\\\".*?\\\")', '\"$1\":\"[REDACTED]\"'\nWrite-Host $safeConfig\n```",
        "pr_file_module": null
      }
    ]
  }
]
