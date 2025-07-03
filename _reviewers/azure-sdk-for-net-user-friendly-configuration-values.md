---
title: User-friendly configuration values
description: Prefer intuitive, user-friendly values for configuration options over
  technical "magic strings" or codes that require special knowledge. This applies
  to both environment variables and programmatic configuration options.
repository: Azure/azure-sdk-for-net
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 5809
---

Prefer intuitive, user-friendly values for configuration options over technical "magic strings" or codes that require special knowledge. This applies to both environment variables and programmatic configuration options.

When designing configuration options:

1. Use descriptive enumeration-like values when possible (e.g., 'global', 'usgov', 'china') rather than requiring users to remember specific technical identifiers
2. Document all valid values explicitly with proper code formatting
3. Support multiple configuration methods for the same setting when appropriate (environment variables and programmatic options)
4. Include clear examples in documentation

**Example:**
```csharp
// Instead of requiring a specific audience string:
clientOptions.AzureCloud = "https://management.azure.com/.default";  // Difficult to remember

// Provide user-friendly enumerated values:
clientOptions.AzureCloud = AzureCloudType.Global;  // More intuitive

// Support both environment variables and programmatic configuration:
// In code:
clientOptions.Diagnostics = { IsTelemetryEnabled = false };

// Or via environment variable (documented in README):
// Set AZURE_TELEMETRY_DISABLED=true
```

For environment variables, document all accepted values and include examples showing both the variable name and possible values.
