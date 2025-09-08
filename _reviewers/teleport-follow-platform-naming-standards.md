---
title: Follow platform naming standards
description: Adhere to established naming conventions specific to each platform, framework,
  or technology being used. Different platforms have different naming requirements
  and best practices that should be followed to ensure compatibility, avoid linter
  warnings, and maintain consistency with ecosystem expectations.
repository: gravitational/teleport
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 19109
---

Adhere to established naming conventions specific to each platform, framework, or technology being used. Different platforms have different naming requirements and best practices that should be followed to ensure compatibility, avoid linter warnings, and maintain consistency with ecosystem expectations.

For Prometheus metrics, avoid suffixes like `_total` for gauge metrics since they are reserved for counter types that only increase:
```
// Incorrect - _total implies counter type
teleport_health_resources_total{type="kubernetes"}

// Correct - no suffix for gauge metrics  
teleport_health_resources{type="kubernetes"}
```

For Kubernetes CRDs, avoid underscores in resource names as they are not allowed:
```yaml
# Incorrect
kind: resource_group

# Correct  
kind: resourcegroup
```

For Protocol Buffer enums, use proper prefixes and avoid generic names like "UNSET":
```protobuf
// Incorrect
enum BotKind {
    UNSET = 0;
    TBOT_BINARY = 1;
}

// Correct
enum BotKind {
    BOT_KIND_UNSPECIFIED = 0;
    BOT_KIND_TBOT_BINARY = 1;
}
```

Research and follow the naming conventions for each technology stack in your project. This prevents compatibility issues, reduces confusion for other developers familiar with those platforms, and ensures tooling works correctly.