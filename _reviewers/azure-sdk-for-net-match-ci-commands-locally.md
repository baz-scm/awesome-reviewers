---
title: Match CI commands locally
description: Always use the same build and test commands locally that are used in
  your CI pipeline to ensure consistency between environments. This practice significantly
  increases the likelihood that code passing locally will also pass in CI, reducing
  integration delays and failed builds.
repository: Azure/azure-sdk-for-net
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 5809
---

Always use the same build and test commands locally that are used in your CI pipeline to ensure consistency between environments. This practice significantly increases the likelihood that code passing locally will also pass in CI, reducing integration delays and failed builds.

For example, instead of using custom build commands or shortcuts, use the exact commands from your pipeline:

```bash
# Instead of:
dotnet build ./myproject.csproj

# Use the CI-equivalent command:
dotnet pack eng/service.proj /p:ServiceDirectory=<service-directory>
dotnet test eng/services.proj /p:ServiceDirectory=<service-directory>
```

This approach helps identify issues earlier in the development process and prevents situations where code passes locally but fails in CI due to environmental differences or non-standard configurations. When everyone on the team follows this practice, it also ensures consistency across developer environments and reduces troubleshooting time for CI failures.
