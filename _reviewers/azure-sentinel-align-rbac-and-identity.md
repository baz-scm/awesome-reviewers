---
title: Align RBAC and Identity
description: When defining permissions or identities in IaC (ARM/CloudFormation/templates),
  ensure the security configuration matches the actual runtime auth path and the provider’s
  supported identity types—avoid “declared-but-unused” privileges and avoid “wrong-scope”
  resources that create authorization or authentication drift.
repository: Azure/Azure-Sentinel
label: Security
language: Json
comments_count: 3
repository_stars: 6042
---

When defining permissions or identities in IaC (ARM/CloudFormation/templates), ensure the security configuration matches the actual runtime auth path and the provider’s supported identity types—avoid “declared-but-unused” privileges and avoid “wrong-scope” resources that create authorization or authentication drift.

Apply this checklist:
- **Verify the runtime authentication method** (e.g., DCR/Logs ingestion via **AAD bearer token** vs using workspace **shared keys**). Don’t grant permissions for mechanisms you don’t use.
- **Prevent cross-artifact mismatches**: if a validator/template requires a field/permission, keep it consistent with the authoritative RBAC source and connector expectations rather than changing one side in isolation.
- **Use supported identity types**: for each resource type, confirm which identity modes are allowed (e.g., `deploymentScripts` supports **UserAssigned**, not **SystemAssigned**). Configure identities accordingly.
- **Keep template scope accurate**: don’t place resources (roles/providers) in the wrong template part; otherwise customers can deploy broken or duplicative security controls.

Example (identity type fix):
```json
{
  "type": "Microsoft.Resources/deploymentScripts",
  "apiVersion": "2020-10-01",
  "name": "WaitSection",
  "location": "<location>",
  "kind": "AzurePowerShell",
  "identity": {
    "type": "UserAssigned",
    "userAssignedIdentities": {
      "<resourceId-of-user-assigned-mi>": {}
    }
  }
}
```
If the script doesn’t need identity, omit `identity` entirely rather than forcing an unsupported identity configuration.