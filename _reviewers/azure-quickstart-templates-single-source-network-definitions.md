---
title: Single Source Network Definitions
description: 'When authoring ARM/Bicep templates, model networking topology as a single
  source of truth and avoid redundant resources/dependencies.


  Apply these rules:'
repository: Azure/azure-quickstart-templates
label: Networking
language: Json
comments_count: 4
repository_stars: 14846
---

When authoring ARM/Bicep templates, model networking topology as a single source of truth and avoid redundant resources/dependencies.

Apply these rules:
1) Define each network object exactly once
- If a subnet is declared under `Microsoft.Network/virtualNetworks.properties.subnets`, do not also create `Microsoft.Network/virtualNetworks/subnets` as a separate child resource.

2) Remove unnecessary explicit dependencies
- If ordering is already implied by references (e.g., workspace → vNet → NSG, load balancer → public IP), don’t add extra `dependsOn`/resource dependencies purely for linkage.

3) Use environment-correct network endpoints
- For services reached over public endpoints, ensure the hostname matches the target environment (example: use `core.usgovcloudapi.net` where required).

Example (ARM): define the subnet only inside the VNet (remove standalone subnet resource)
```json
{
  "type": "Microsoft.Network/virtualNetworks",
  "apiVersion": "2020-11-01",
  "name": "[parameters('vnetName')]",
  "location": "[parameters('location')]",
  "properties": {
    "addressSpace": { "addressPrefixes": ["[parameters('vnetAddressPrefix')]" ] },
    "subnets": [
      {
        "name": "[parameters('hsmSubnetName')]",
        "properties": {
          "addressPrefix": "[parameters('hsmSubnetPrefix')]",
          "delegations": [
            {
              "name": "Microsoft.HardwareSecurityModules.dedicatedHSMs",
              "properties": {
                "serviceName": "Microsoft.HardwareSecurityModules/dedicatedHSMs"
              }
            }
          ]
        }
      }
    ]
  }
}
// Do NOT also declare Microsoft.Network/virtualNetworks/subnets for that subnet.
```

Outcome: fewer deployment conflicts, simpler dependency graphs, and more predictable networking behavior across environments.