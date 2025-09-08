---
title: Network address clarity
description: When documenting or configuring network addresses, DNS names, and IP
  addresses, be explicit about traffic direction and ensure uniqueness to prevent
  conflicts and ambiguity.
repository: gravitational/teleport
label: Networking
language: Other
comments_count: 2
repository_stars: 19109
---

When documenting or configuring network addresses, DNS names, and IP addresses, be explicit about traffic direction and ensure uniqueness to prevent conflicts and ambiguity.

For IP addresses, specify whether they are for ingress or egress traffic:
```yaml
# Good: Explicit about traffic direction
Teleport Cloud maintains a list of IP addresses it uses for ingress. If your environment restricts outbound traffic,

# Avoid: Ambiguous traffic direction
Teleport Cloud maintains a list of IP addresses it uses. If your environment restricts outbound traffic,
```

For DNS names and public addresses, ensure they are unique and don't conflict with existing cluster addresses:
```yaml
- name: "jira"
  uri: "https://localhost:8001"
  # The public address must be a unique DNS name and not conflict with the Teleport cluster's public addresses.
```

This prevents network configuration errors, reduces troubleshooting time, and makes network architecture clearer for both developers and operators.