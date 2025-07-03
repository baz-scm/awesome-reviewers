---
title: Fail fast principle
description: Design CI/CD pipelines to fail quickly and visibly rather than masking
  errors through excessive retries or complex conditions. When a build step fails,
  it should fail immediately with clear error reporting to reduce debugging time and
  enable faster remediation.
repository: chef/chef
label: CI/CD
language: Other
comments_count: 3
repository_stars: 7860
---

Design CI/CD pipelines to fail quickly and visibly rather than masking errors through excessive retries or complex conditions. When a build step fails, it should fail immediately with clear error reporting to reduce debugging time and enable faster remediation.

Instead of implementing multiple retry attempts that delay the inevitable failure, prefer a minimal retry strategy or a single attempt with good error logging. This approach reduces build time and exposes problems sooner, allowing developers to address issues more efficiently.

For example, replace code like this:
```
$install_attempt = 0
do {
    Start-Sleep -Seconds 5
    $install_attempt++
    Write-BuildLine "Install attempt $install_attempt"
    bundle exec rake install:local --trace=stdout
} while ((-not $?) -and ($install_attempt -lt 5))
```

With a simpler approach:
```
bundle exec rake install --trace=stdout
```

Similarly, when configuring pipeline conditions, use concise regex patterns that are easy to understand and maintain rather than complex, hard-to-read conditions that might hide logic errors.
