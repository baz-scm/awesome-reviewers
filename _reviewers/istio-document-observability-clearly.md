---
title: Document observability clearly
description: Ensure observability documentation is clear, accessible, and grammatically
  correct. This includes defining technical acronyms and ensuring proper sentence
  structure in configuration explanations.
repository: istio/istio
label: Observability
language: Markdown
comments_count: 2
repository_stars: 37192
---

Ensure observability documentation is clear, accessible, and grammatically correct. This includes defining technical acronyms and ensuring proper sentence structure in configuration explanations.

When documenting observability systems, always:
- Define technical acronyms on first use with links to official documentation when available
- Use proper grammar and clear sentence structure in configuration explanations
- Ensure warnings and notes about system behavior are unambiguous

Example of good practice:
```markdown
# Open Telemetry ALS with Loki

This sample demonstrates Access Log Service (ALS) integration with Loki for distributed tracing.

> **Warning**   
> When the example `PodMonitor` is used with OpenShift Monitoring, it must be created in all namespaces where istio-proxies exist.  
> This is because `namespaceSelector` is ignored for tenancy isolation.
```

Clear documentation prevents misconfigurations and reduces support overhead in observability deployments.