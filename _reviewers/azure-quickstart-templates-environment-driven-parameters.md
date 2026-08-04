---
title: Environment-Driven Parameters
description: 'When a template needs configuration that varies by environment/cloud/region
  or depends on real resource identifiers, do not hardcode endpoints/locations or
  fabricate subscription/RG paths. Instead:'
repository: Azure/azure-quickstart-templates
label: Configurations
language: Json
comments_count: 8
repository_stars: 14846
---

When a template needs configuration that varies by environment/cloud/region or depends on real resource identifiers, do not hardcode endpoints/locations or fabricate subscription/RG paths. Instead:
- Derive environment-specific endpoints from the selected cloud/environment config (e.g., use a cloud config map and reference it in resource definitions).
- Require user-supplied values for resource identifiers that are resource-path-like (and validate prerequisites); avoid using placeholder tokens (e.g., “GEN-UNIQUE”) unless your CI/test tooling explicitly substitutes them.
- Avoid changing uniqueness behavior for identifiers like DNS label prefixes that must remain unique in the target scope.
- Use safe defaults only when the feature is globally available and the default region/values won’t break deployments; otherwise use allowedValues or remove defaults.

Example (cloud endpoints):
```json
{
  "parameters": {
    "cloudEnvironment": {
      "type": "string",
      "defaultValue": "Public",
      "allowedValues": ["Public","USGovernment","China"]
    }
  },
  "variables": {
    "cloudConfig": {
      "Public": { "graph": "https://graph.microsoft.com" },
      "USGovernment": { "graph": "https://graph.microsoft.us" },
      "China": { "graph": "https://microsoftgraph.chinacloudapi.cn" }
    },
    "cloud": "[variables('cloudConfig')[parameters('cloudEnvironment')]]"
  },
  "resources": [
    {
      "type": "Microsoft.Logic/workflows",
      "properties": {
        "definition": {
          "parameters": {
            "graphEndpoint": {
              "type": "String",
              "defaultValue": "[variables('cloud').graph]"
            }
          }
        }
      }
    }
  ]
}
```

Example (resource IDs/paths): if a parameter is expected to be a full resource path, document it as a prerequisite and accept it as-is; do not attempt to construct subscription/RG IDs randomly in parameters—use ARM functions like `resourceId()` inside the template when you need IDs from context.