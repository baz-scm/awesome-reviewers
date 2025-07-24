---
title: API field documentation
description: API fields must be comprehensively documented with clear behavior specifications,
  format constraints, and interaction details. This includes documenting how fields
  interact with each other, specifying allowed formats and validation rules, clarifying
  field semantics and placement decisions, and aligning naming conventions with existing
  Kubernetes APIs.
repository: kubernetes/kubernetes
label: API
language: Go
comments_count: 8
repository_stars: 116489
---

API fields must be comprehensively documented with clear behavior specifications, format constraints, and interaction details. This includes documenting how fields interact with each other, specifying allowed formats and validation rules, clarifying field semantics and placement decisions, and aligning naming conventions with existing Kubernetes APIs.

Key documentation requirements:
- Document field interactions: "document how this interacts with `Count` when `Count` is > 1 ... are these capacityRequests per device or across devices?"
- Specify format constraints: "Describe the allowed format for values in this field" and "Note that only one DeviceClass should specify this extended resource name"
- Clarify field semantics: Choose field names that align with existing conventions (e.g., using "requests" to match container resource terminology rather than inventing new terms like "minimum")
- Document field placement rationale: Consider immutability requirements when deciding between placing fields in AllocationResult vs status fields

Example of proper field documentation:
```go
// CapacityRequests define resource requirements against each capacity.
// When Count > 1, these requirements apply per device.
// When allocationMode=All, this selects all matching devices which can satisfy the capacityRequests.
//
// +optional
// +featureGate=DRAConsumableCapacity
CapacityRequests *CapacityRequirements

// ExtendedResourceName is the extended resource name for devices of this class.
// Must be a valid extended resource name format (domain/resource-name).
// Only one DeviceClass should specify the same extendedResourceName.
// If multiple DeviceClasses specify the same name, scheduling behavior is undefined.
//
// +optional
// +featureGate=DRAExtendedResources
ExtendedResourceName *string
```

This practice prevents confusion during API evolution, ensures consistent behavior across implementations, and provides clear guidance for API consumers.