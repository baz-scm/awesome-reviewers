---
title: Stable observability components
description: Always use stable, production-ready versions of observability components
  (libraries, dependencies, and documentation references) in your applications. Monitoring
  and observability systems are critical infrastructure that should prioritize stability
  over cutting-edge features.
repository: spring-projects/spring-boot
label: Observability
language: Other
comments_count: 2
repository_stars: 77637
---

Always use stable, production-ready versions of observability components (libraries, dependencies, and documentation references) in your applications. Monitoring and observability systems are critical infrastructure that should prioritize stability over cutting-edge features.

For libraries:
- Avoid alpha, beta, or milestone releases in production code
- Test compatibility with your entire observability stack before upgrading
- Consider downstream dependencies that might be affected

For documentation and references:
- Link to specific stable versions (tags or SHAs) rather than main branches

Example of what to avoid:
```gradle
library("OpenTelemetry", "1.23.1-alpha") {  // Problematic: alpha version
    group("io.opentelemetry") {
        imports = [
            "opentelemetry-bom-alpha"       // Indicates unstable release
        ]
    }
}
```

Instead, use stable versions:
```gradle
library("OpenTelemetry", "1.19.0") {  // Stable version
    group("io.opentelemetry") {
        imports = [
            "opentelemetry-bom"            // Standard stable artifact
        ]
    }
}
```

This approach helps ensure your monitoring systems remain reliable and don't introduce unexpected behavior when capturing critical operational data.