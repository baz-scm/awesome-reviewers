---
title: Conservative networking defaults
description: When configuring networking components, prefer stable and permissive
  defaults over restrictive or experimental configurations that may not work across
  all environments. This approach ensures broader compatibility and reduces the risk
  of breaking existing deployments.
repository: istio/istio
label: Networking
language: Yaml
comments_count: 5
repository_stars: 37192
---

When configuring networking components, prefer stable and permissive defaults over restrictive or experimental configurations that may not work across all environments. This approach ensures broader compatibility and reduces the risk of breaking existing deployments.

Key principles:
- Use permissive network policies that work across different cluster configurations rather than restrictive rules that assume specific API server locations or ports
- Default to well-tested networking modes (like iptables) rather than newer alternatives (like eBPF) until they have sufficient testing and compatibility
- Implement new networking features as fallbacks or opt-in capabilities rather than replacing existing stable functionality
- Ensure network configuration changes maintain backward compatibility to avoid breaking existing user setups

Example from NetworkPolicy configuration:
```yaml
egress:
# Allow all egress traffic by default rather than restrictive rules
- {}
```

This approach prioritizes system stability and broad compatibility over maximum security or cutting-edge features, allowing users to customize and lock down configurations based on their specific requirements and environments.