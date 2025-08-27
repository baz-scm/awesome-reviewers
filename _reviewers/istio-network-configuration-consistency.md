---
title: network configuration consistency
description: Ensure network-related configurations remain consistent across different
  components and avoid unintended overwrites that could break connectivity or security.
repository: istio/istio
label: Networking
language: Go
comments_count: 5
repository_stars: 37192
---

Ensure network-related configurations remain consistent across different components and avoid unintended overwrites that could break connectivity or security.

When modifying network configurations, always consider the impact on related components and use appropriate update mechanisms:

1. **Use Server-Side Apply (SSA) instead of direct updates** to prevent overwriting existing configurations:
```go
// Instead of direct update that overwrites
service.ResourceVersion = existingService.ResourceVersion
_, err = svcClient.Update(service)

// Use patch or SSA to merge configurations
patchBytes, err = c.generateShadowServicePatch(existingService, service)
_, err = svcClient.Patch(existingService.Name, existingService.Namespace, types.MergePatchType, patchBytes)
```

2. **Maintain consistency in DNS and network settings** across bootstrap and dynamic configurations:
```go
// Ensure DNS lookup family settings match between bootstrap and cluster builder
if networkutil.AllIPv4(cb.proxyIPAddresses) {
    c.DnsLookupFamily = cluster.Cluster_V4_ONLY
} else if networkutil.AllIPv6(cb.proxyIPAddresses) {
    c.DnsLookupFamily = cluster.Cluster_V6_ONLY
} else {
    // Dual Stack - use consistent logic across components
    c.DnsLookupFamily = cluster.Cluster_ALL
}
```

3. **Merge configurations rather than replace** when updating network filters or options to preserve existing functionality:
```go
// Merge HTTP1 options to avoid overwriting existing settings
setHTTP1Options(cluster, effectiveProxyConfig.GetProxyHeaders().GetPreserveHttp1HeaderCase())
```

This prevents network connectivity issues, security vulnerabilities, and configuration drift that can occur when components have inconsistent network settings or when updates inadvertently overwrite critical configurations.