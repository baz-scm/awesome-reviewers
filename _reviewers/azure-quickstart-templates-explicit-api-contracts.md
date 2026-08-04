---
title: Explicit API Contracts
description: 'When authoring templates or clients that call/describe APIs (Graph,
  resource providers, etc.), treat the “API contract” as a first-class design artifact:'
repository: Azure/azure-quickstart-templates
label: API
language: Json
comments_count: 7
repository_stars: 14846
---

When authoring templates or clients that call/describe APIs (Graph, resource providers, etc.), treat the “API contract” as a first-class design artifact:

- **Do not parameterize `apiVersion`** in the consumer-facing surface unless you have a **planned compatibility/back-compat story**; prefer hardcoding and only change versions intentionally.
- **Avoid opaque payload parameterization**: don’t pass an entire `properties` body as a single parameter value. Instead, parameterize the individual fields (or use a single `object` parameter type only when you truly need to accept a structured payload).
- **Group related request/trigger/type constants** into a cohesive contract object so the API shape is obvious and maintainable.
- **Compose resource identifiers with `resourceId(...)`** (deterministic, correct segments) instead of brittle string concatenation.

Example patterns:

- Prefer a cohesive contract object for trigger/type mapping:
```json
"triggerType": {
  "dataOdataTypeExpression": "@{triggerBody()?['data']?['@odata.type']}",
  "uploadDataType": "#microsoft.graph.customDataProvidedResourceRequestAccessReviewDataCalloutData",
  "applyDecisionType": "#microsoft.graph.customDataProvidedResourceApplyDecisionContextData",
  "updateAccessAssignmentType": "#microsoft.graph.customDataProvidedResourceAccessAssignmentCalloutData"
}
```

- Prefer explicit property parameterization over passing whole payloads:
```json
"parameters": {
  "targetProperties": { "type": "array" }
}
// and then use json()/field-wise mapping in the resource, rather than passing
// a single opaque `properties` object string/blob as the parameter value.
```

- Hardcode `apiVersion` (or only expose it with a deliberate compatibility plan):
```json
"apiVersion": "2023-05-02"
```

- Use structured `resourceId(...)` for API-facing resource identifiers:
```json
"proximityPlacementGroup": "[resourceId(parameters('ProximityPlacementGroupResourceGroup'),'Microsoft.Compute/proximityPlacementGroups', parameters('ProximityPlacementGroupName'))]"
```