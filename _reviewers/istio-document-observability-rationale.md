---
title: Document observability rationale
description: When introducing, modifying, or removing observability features (tracing,
  metrics, monitoring configurations), always include clear documentation explaining
  the rationale, use cases, and migration guidance. Users need to understand why they
  would want to use a feature and how it solves their specific problems.
repository: istio/istio
label: Observability
language: Yaml
comments_count: 4
repository_stars: 37192
---

When introducing, modifying, or removing observability features (tracing, metrics, monitoring configurations), always include clear documentation explaining the rationale, use cases, and migration guidance. Users need to understand why they would want to use a feature and how it solves their specific problems.

For new features, explain the problem being solved and provide usage examples. For configuration changes, document the migration path and any behavioral differences. For removals, clearly state alternatives and upgrade steps.

Example from release notes:
```yaml
releaseNotes:
  - |
    **Added** environment variable `PILOT_SPAWN_UPSTREAM_SPAN_FOR_GATEWAY`, 
    which separates tracing span for both server and client gateways. 
    This currently defaults to false but will become default in the future.
    
    Use this when you need separate visibility into gateway request 
    processing stages for better debugging and performance analysis.
```

This approach helps teams make informed decisions about their observability stack and reduces confusion during upgrades or configuration changes.