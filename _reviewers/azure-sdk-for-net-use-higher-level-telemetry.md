---
title: Use higher-level telemetry
description: When implementing observability for Azure services, prefer higher-level
  telemetry packages and configuration methods over low-level implementations. For
  Azure Monitor integration, use the Azure.Monitor.OpenTelemetry.AspNetCore package
  instead of the lower-level Azure.Monitor.OpenTelemetry.Exporter, as it provides
  simpler integration and is the recommended...
repository: Azure/azure-sdk-for-net
label: Observability
language: Markdown
comments_count: 2
repository_stars: 5809
---

When implementing observability for Azure services, prefer higher-level telemetry packages and configuration methods over low-level implementations. For Azure Monitor integration, use the Azure.Monitor.OpenTelemetry.AspNetCore package instead of the lower-level Azure.Monitor.OpenTelemetry.Exporter, as it provides simpler integration and is the recommended approach for most scenarios.

For enabling OpenTelemetry support, you can use either environment variables or programmatic configuration:

```csharp
// Option 1: Set environment variable (before application starts)
// AZURE_EXPERIMENTAL_ENABLE_ACTIVITY_SOURCE=true

// Option 2: Use AppContext.SetSwitch (preferred for programmatic control)
AppContext.SetSwitch("Azure.Experimental.EnableActivitySource", true);

// Use the recommended higher-level package
// Install: dotnet add package Azure.Monitor.OpenTelemetry.AspNetCore
// Instead of the lower-level: Azure.Monitor.OpenTelemetry.Exporter
```

Using higher-level telemetry packages simplifies implementation, provides better defaults, and follows Azure SDK best practices for observability. This approach reduces the complexity of monitoring code and improves maintainability while ensuring comprehensive system visibility.
