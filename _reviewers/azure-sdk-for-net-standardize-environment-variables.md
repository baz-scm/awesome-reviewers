---
title: Standardize environment variables
description: Ensure environment variable names are consistently spelled, properly
  referenced, and follow established naming conventions across test files. Replace
  hardcoded values with environment variables for credentials, endpoints, and other
  configurable test parameters. Always provide meaningful defaults when environment
  variables aren't available to ensure tests...
repository: Azure/azure-sdk-for-net
label: Configurations
language: C#
comments_count: 4
repository_stars: 5809
---

Ensure environment variable names are consistently spelled, properly referenced, and follow established naming conventions across test files. Replace hardcoded values with environment variables for credentials, endpoints, and other configurable test parameters. Always provide meaningful defaults when environment variables aren't available to ensure tests can run in various environments.

```csharp
// Instead of hardcoding test values:
var principalId = "22fdaec1-8b9f-49dc-bd72-ddaf8f215577";
var tenantId = "72f988af-86f1-41af-91ab-2d7cd011db47";
var connectionId = TestEnvironment.SHAREPOINT_CONECTION_ID; // Typo!

// Use environment variables with fallbacks and correct naming:
var principalId = Environment.GetEnvironmentVariable("TEST_PRINCIPAL_ID") ?? "22fdaec1-8b9f-49dc-bd72-ddaf8f215577";
var tenantId = Environment.GetEnvironmentVariable("TEST_TENANT_ID") ?? "72f988af-86f1-41af-91ab-2d7cd011db47";
var connectionId = TestEnvironment.SHAREPOINT_CONNECTION_ID; // Fixed spelling
```

When defining environment variable names in test environments or documentation, follow consistent naming patterns like using all caps with underscores for separators. Double-check for typos, as misspelled environment variable names will silently return null values and may cause tests to fail in unexpected ways.
