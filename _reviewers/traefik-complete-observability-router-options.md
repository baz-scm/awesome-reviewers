---
title: complete observability router options
description: When documenting router configuration options for any provider (Docker,
  Consul Catalog, ECS, KV stores, Nomad, etc.), ensure that all observability-related
  router options are included and properly documented. This is critical for enabling
  comprehensive monitoring, tracing, and logging capabilities.
repository: traefik/traefik
label: Observability
language: Markdown
comments_count: 6
repository_stars: 55772
---

When documenting router configuration options for any provider (Docker, Consul Catalog, ECS, KV stores, Nomad, etc.), ensure that all observability-related router options are included and properly documented. This is critical for enabling comprehensive monitoring, tracing, and logging capabilities.

The following observability router options must be documented for each provider:

```yaml
# Access logs control
traefik.http.routers.<router_name>.observability.accesslogs=true

# Distributed tracing control  
traefik.http.routers.<router_name>.observability.tracing=true

# Metrics collection control
traefik.http.routers.<router_name>.observability.metrics=true
```

These options allow developers to enable or disable specific observability features at the router level, providing fine-grained control over monitoring and debugging capabilities. Without proper documentation of these options, developers cannot effectively configure observability for their services.

Additionally, when documenting router-level observability, clarify the relationship with global settings: "To enable router-level observability, you must first enable access-logs, tracing, and metrics globally. When metrics layers are not enabled with the `addEntryPointsLabels`, `addRoutersLabels` and/or `addServicesLabels` options, enabling metrics for a router will not enable them."

This ensures developers understand both the configuration options available and the prerequisites for their effective use.