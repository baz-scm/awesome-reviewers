---
title: Avoid Hardcoded Environments
description: Do not commit configuration that is (a) unnecessary/stale or (b) hardcoded
  to specific environments (e.g., `gamma`, `beta`, `no-prod`, or other prod variants).
  Keep repo configuration environment-agnostic by parameterizing values and deriving
  environment-specific behavior at runtime/deployment.
repository: awslabs/agentcore-samples
label: Configurations
language: Json
comments_count: 2
repository_stars: 3244
---

Do not commit configuration that is (a) unnecessary/stale or (b) hardcoded to specific environments (e.g., `gamma`, `beta`, `no-prod`, or other prod variants). Keep repo configuration environment-agnostic by parameterizing values and deriving environment-specific behavior at runtime/deployment.

Apply it:
- If a config file isn’t actively used, remove it and update documentation/build/deployment references accordingly.
- If a config must exist (e.g., endpoint definitions), ensure it does not contain literal environment identifiers. Use a generic parameter (like `stage`) and map/compute environment-specific URLs outside the committed config.

Example standard (environment-agnostic shape):
```json
{
  "parameters": {
    "endpoint": { "type": "String", "documentation": "Override endpoint" },
    "region": { "type": "String", "default": "us-east-1" },
    "stage": { "type": "String", "documentation": "Deployment stage" }
  },
  "rules": [
    {
      "type": "endpoint",
      "conditions": [{"fn":"isSet","argv":[{"ref":"endpoint"}]}],
      "endpoint": { "url": "{endpoint}" }
    }
  ]
}
```
Ensure no committed config contains fixed strings like `gamma`/`beta`/`no-prod`; if behavior depends on them, handle it via deployment-time variables or a controlled mapping layer.