---
title: Configure OpenTelemetry programmatically
description: Configure OpenTelemetry programmatically rather than through environment
  variables or command-line flags. This creates a more maintainable and standardized
  approach to observability. Additionally, ensure all observability components like
  collectors are explicitly included in your deployment configurations.
repository: temporalio/temporal
label: Observability
language: Yaml
comments_count: 2
repository_stars: 14953
---

Configure OpenTelemetry programmatically rather than through environment variables or command-line flags. This creates a more maintainable and standardized approach to observability. Additionally, ensure all observability components like collectors are explicitly included in your deployment configurations.

Example:
```yaml
# Preferred - Adding collector to Docker Compose services
{% raw %}
services: "${{ format('{0}\notel-collector', join(matrix.containers, '\n')) }}"
{% endraw %}

# Avoid passing as environment variables
# make OTEL=true functional-test-coverage  # Not recommended
```

This approach ensures consistent observability setup across environments and makes configuration changes more traceable through source control.