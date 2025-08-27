---
title: telemetry consistency standards
description: Ensure telemetry attribute population logic is consistent across all
  components and follows established standards. When implementing telemetry features
  like resource attributes, baggage headers, or tracing configurations, use the same
  business logic and attribute naming conventions throughout the codebase.
repository: istio/istio
label: Observability
language: Go
comments_count: 4
repository_stars: 37192
---

Ensure telemetry attribute population logic is consistent across all components and follows established standards. When implementing telemetry features like resource attributes, baggage headers, or tracing configurations, use the same business logic and attribute naming conventions throughout the codebase.

Key requirements:
1. **Follow OpenTelemetry semantic conventions**: Always adhere to official OpenTelemetry Resource Semantic Conventions for attribute naming and structure
2. **Maintain cross-component consistency**: Use identical logic for populating telemetry attributes across different implementations (baggage processing, resource attributes, tracing, etc.)
3. **Align with external specifications**: Reference and follow established standards from OpenTelemetry, Envoy, and other external systems

Example of consistent attribute population:
```go
// Use the same logic across components
func resourceAttributes(proxy *Proxy) *otlpcommon.KeyValueList {
    return &otlpcommon.KeyValueList{
        Values: []*otlpcommon.KeyValue{
            // Use OpenTelemetry semantic convention constants
            otelKeyValue(otelsemconv.K8SClusterNameKey, proxy.Metadata.ClusterID.String()),
            otelKeyValue(otelsemconv.K8SNamespaceNameKey, proxy.ConfigNamespace),
            otelKeyValue(otelsemconv.K8SPodNameKey, podName),
            otelKeyValue(otelsemconv.ServiceNameKey, proxy.XdsNode.Cluster),
        },
    }
}
```

This approach prevents inconsistencies that can lead to fragmented telemetry data and ensures compliance with industry standards, making the observability system more reliable and interoperable.