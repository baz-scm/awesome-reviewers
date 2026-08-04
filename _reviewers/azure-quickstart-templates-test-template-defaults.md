---
title: Test template defaults
description: When testing a template’s behavior, avoid overriding it with explicit
  parameter values. Remove parameter values from the parameters file so the template’s
  `defaultValue(s)` are used, ensuring the default-path is actually exercised.
repository: Azure/azure-quickstart-templates
label: Testing
language: Json
comments_count: 2
repository_stars: 14846
---

When testing a template’s behavior, avoid overriding it with explicit parameter values. Remove parameter values from the parameters file so the template’s `defaultValue(s)` are used, ensuring the default-path is actually exercised.

Example (parameters file):
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "someParam": {
      "// omit "value" here to use template defaultValue"
    }
  }
}
```

Only provide `value` fields when intentionally testing non-default behavior; otherwise leave them out to validate defaults.