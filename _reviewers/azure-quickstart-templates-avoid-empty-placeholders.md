---
title: Avoid empty placeholders
description: When a parameter/property is optional in an ARM template, don’t represent
  “missing” with empty objects or empty strings—these can be treated as real values
  and fail validation or downstream logic.
repository: Azure/azure-quickstart-templates
label: Null Handling
language: Json
comments_count: 4
repository_stars: 14846
---

When a parameter/property is optional in an ARM template, don’t represent “missing” with empty objects or empty strings—these can be treated as real values and fail validation or downstream logic.

Apply these rules:
- **Resource `properties`:** Don’t add `properties: {}` unless the schema truly requires it. If ARM reports “missing properties,” ensure the required shape exists; otherwise omit empty objects.
- **String parameters (null-equivalent):** Avoid `"defaultValue": ""` for optional string parameters if the deployment engine/template logic treats an empty string as a value (causing errors like missing keys). Prefer **omitting** the parameter when not provided, or use ARM conditional logic to set the target field only when the parameter is non-empty.
- **Defaults vs environment:** Only set/use `defaultValue` in templates/parameters when it’s valid for the target environment globally. To verify defaults work, remove overrides in `azuredeploy.parameters.json` so default behavior is exercised.

Example (pattern):
```json
{
  "parameters": {
    "adminPublicKey": { "type": "string" }
  },
  "variables": {
    "adminPublicKeyValue": "[if(empty(parameters('adminPublicKey')), json('null'), parameters('adminPublicKey'))]"
  }
  // Then assign the SSH key only when not null/empty (or handle it in template logic).
}
```
If you use empty-string defaults for testing, ensure CI/pipeline parameter files still provide valid required values (don’t rely on `""` to represent “not provided”).