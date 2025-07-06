---
title: Consistent API versioning approach
description: 'Adopt and document a consistent approach to API versioning across your
  services. The chosen format should be clearly communicated, whether using the simple
  form (e.g., `"apiVersion": "v0alpha1"`) or the fully qualified form (e.g., `"apiVersion":
  "prometheus.datasource.grafana.app/v0alpha1"`).'
repository: grafana/grafana
label: API
language: Go
comments_count: 4
repository_stars: 68825
---

Adopt and document a consistent approach to API versioning across your services. The chosen format should be clearly communicated, whether using the simple form (e.g., `"apiVersion": "v0alpha1"`) or the fully qualified form (e.g., `"apiVersion": "prometheus.datasource.grafana.app/v0alpha1"`).

When exposing API version information:

1. Document which format clients should expect and use
2. Consider how version information will be consumed by clients
3. Ensure that API specifications (OpenAPI) and implementations are aligned
4. Remember that resources may support multiple API versions

```go
// When defining API resources, be explicit about version requirements
type ResourceDefinition struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata"` // Required fields should not use omitempty
    
    // If using OpenAPI generation, ensure annotations match expected behavior
    // +optional
    APIVersion string `json:"apiVersion,omitempty"`
    
    // Other fields...
}
```

Clients should be designed with the understanding that API resources may expose multiple versions, and avoid making assumptions about specific version formats. This promotes API stability and enables easier version transitions.