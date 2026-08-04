---
title: Deterministic Resource Naming
description: Use deterministic, semantically correct identifiers for ARM template
  parameters and resource names—especially where idempotency and uniqueness are required.
repository: Azure/azure-quickstart-templates
label: Naming Conventions
language: Json
comments_count: 7
repository_stars: 14846
---

Use deterministic, semantically correct identifiers for ARM template parameters and resource names—especially where idempotency and uniqueness are required.

Rules:
1. Match the expected identifier shape
   - If a parameter/property expects a resource ID path, provide the full ARM resource ID (e.g., "/subscriptions/<subId>/resourcegroups/<rg>/providers/<type>/<name>")—don’t use generic placeholders like "GEN-UNIQUE".
2. Use the correct placeholder token
   - For credentials, use the password placeholder (e.g., "GEN-PASSWORD"), not "GEN-UNIQUE".
   - For length-limited names, use a bounded placeholder (e.g., "GEN-UNIQUE-15") to avoid invalid identifiers.
3. Make roleAssignment names idempotent
   - For Microsoft.Authorization/roleAssignments, set the assignment resource name using guid() seeded with the exact principalId (full principal resourceId or objectId), roleId (full roleDefinition resourceId), and scopeId (full scope resourceId).

Example pattern:
```json
{
  "type": "Microsoft.Authorization/roleAssignments",
  "apiVersion": "2020-04-01-preview",
  "name": "[concat('Microsoft.Authorization/', guid(
    variables('principalId'),
    variables('roleId'),
    variables('scopeId')
  ))]",
  "properties": {
    "principalId": "[variables('principalId')]",
    "roleDefinitionId": "[variables('roleId')]",
    "scope": "[variables('scopeId')]"
  }
}
```

4. Preserve required string formatting
   - When building scope/resource strings via concat(), ensure the exact expected path separators (slashes) are present (e.g., "/virtualMachines/<vmName>").