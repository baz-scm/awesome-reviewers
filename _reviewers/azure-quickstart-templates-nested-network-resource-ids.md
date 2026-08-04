---
title: Nested Network Resource IDs
description: 'When working with Azure networking in Bicep, avoid “stringly” nested
  resource references built from `resourceId()` plus `dependsOn`. Instead:


  1) **Define subnets idempotently**: create subnets inside the `virtualNetworks`
  resource via `properties.subnets`.'
repository: Azure/azure-quickstart-templates
label: Networking
language: Other
comments_count: 7
repository_stars: 14846
---

When working with Azure networking in Bicep, avoid “stringly” nested resource references built from `resourceId()` plus `dependsOn`. Instead:

1) **Define subnets idempotently**: create subnets inside the `virtualNetworks` resource via `properties.subnets`.
2) **Reference nested resources safely**: when another resource needs a subnet / inboundNatRule / probe / backend pool id, declare it as an **`existing` child resource** and use `childResource.id`.
3) **Use correct nested resource `resourceId` shapes** for LB sub-components (frontend/backends/probes) rather than manual concatenation.

Example (subnet + LB NAT rule):

```bicep
param location string = resourceGroup().location
param vnetName string = 'myVnet'
param subnetName string = 'subnet1'
param lbName string = 'myLB'

resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: subnetName
        properties: {
          addressPrefix: '10.0.0.0/24'
        }
      }
    ]
  }
}

resource lb 'Microsoft.Network/loadBalancers@2024-01-01' = {
  name: lbName
  location: location
  properties: {
    // ...
    inboundNatRules: [
      {
        name: 'RDP-VM0'
        properties: {
          protocol: 'Tcp'
          frontendPort: 50001
          backendPort: 3389
        }
      }
    ]
  }
}

resource subnetRef 'Microsoft.Network/virtualNetworks/subnets@2024-01-01' existing = {
  parent: vnet
  name: subnetName
}

resource inboundNatRuleRef 'Microsoft.Network/loadBalancers/inboundNatRules@2024-01-01' existing = {
  parent: lb
  name: 'RDP-VM0'
}

resource nic 'Microsoft.Network/networkInterfaces@2024-01-01' = {
  name: 'nic1'
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          subnet: { id: subnetRef.id }
          loadBalancerInboundNatRules: [
            { id: inboundNatRuleRef.id }
          ]
        }
      }
    ]
  }
}
```

This approach improves redeploy reliability (subnets don’t break on re-apply) and improves correctness/maintainability (nested ids are sourced from typed resource declarations instead of hand-built IDs and fragile dependency wiring).