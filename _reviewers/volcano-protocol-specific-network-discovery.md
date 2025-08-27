---
title: Protocol-specific network discovery
description: When implementing network topology discovery features, use discovery
  methods that are appropriate for the specific network protocol being used. Different
  network protocols have different architectures and require different approaches
  for topology discovery.
repository: volcano-sh/volcano
label: Networking
language: Markdown
comments_count: 2
repository_stars: 4899
---

When implementing network topology discovery features, use discovery methods that are appropriate for the specific network protocol being used. Different network protocols have different architectures and require different approaches for topology discovery.

For centralized management protocols like UFM (Unified Fabric Manager), use endpoint-based configuration to connect to the central management interface. For distributed protocols like RoCE (RDMA over Converged Ethernet), use distributed discovery methods such as LLDP (Link Layer Discovery Protocol) to collect neighbor information from each node and switch, then reconstruct the full topology.

For InfiniBand networks, leverage tools like `ibnetdiscover` for topology discovery. For RoCE environments, consider using LLDP-based tools like lldpd or similar open-source alternatives on the node side.

Example configuration showing protocol-appropriate approaches:

```yaml
discoveryConfig:
  - source: ufm  # Centralized management
    enabled: true
    config:
      endpoint: https://ufm-server:8080
      username: admin
      password: password
  - source: roce  # Distributed discovery
    enabled: true
    config:
      # Uses LLDP-based discovery, may require daemonset deployment
      discoveryMethod: lldp
```

Be aware that switch support and access methods can vary significantly between vendors, which may require vendor-specific contributions or adaptations for full compatibility.