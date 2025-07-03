---
title: Use domain-specific type names
description: Types should be named with clear domain context rather than generic terms.
  Avoid single-word or overly generic names that could be ambiguous or conflict with
  other types. Instead, prefix type names with their domain or service name to provide
  clear context and prevent naming collisions.
repository: Azure/azure-sdk-for-net
label: Naming Conventions
language: C#
comments_count: 6
repository_stars: 5809
---

Types should be named with clear domain context rather than generic terms. Avoid single-word or overly generic names that could be ambiguous or conflict with other types. Instead, prefix type names with their domain or service name to provide clear context and prevent naming collisions.

Example - Instead of:
```csharp
public class ConnectorData { }
public class Performance { }
public class HttpGet { }
```

Use domain-specific names:
```csharp
public class ImpactReportingConnector { }
public class WorkloadPerformanceMetrics { }
public class HttpGetOperation { }
```

This makes the code more maintainable by:
- Preventing naming conflicts across different services/domains
- Making type purposes immediately clear from their names
- Improving code searchability and navigation
- Reducing cognitive load when reading code
