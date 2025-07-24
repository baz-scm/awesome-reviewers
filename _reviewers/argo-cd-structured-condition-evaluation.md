---
title: structured condition evaluation
description: When implementing health checks, use comprehensive condition evaluation
  patterns instead of simple field comparisons. Check multiple condition attributes
  (type, status, reason, message) to ensure accurate health status determination.
repository: argoproj/argo-cd
label: Observability
language: Other
comments_count: 2
repository_stars: 20149
---

When implementing health checks, use comprehensive condition evaluation patterns instead of simple field comparisons. Check multiple condition attributes (type, status, reason, message) to ensure accurate health status determination.

Simple field checks can miss important state information and lead to incorrect health assessments. Instead of checking a single ready field, evaluate the full condition structure to get a complete picture of resource health.

Example of preferred approach:
```lua
if obj.status ~= nil and obj.status.conditions ~= nil then
  for _, condition in ipairs(obj.status.conditions) do
    if condition.type == "Ready" and condition.status == "True" and condition.reason == "Succeeded" then
      hs.status = "Healthy"
      return hs
    end
  end
end
```

Avoid oversimplified checks like `if obj.status.ready == "true"` or `if obj.status.ready then` when structured conditions are available. This pattern improves observability by providing more reliable health status reporting and better debugging information when issues occur.