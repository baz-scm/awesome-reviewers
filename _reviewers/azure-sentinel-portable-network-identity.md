---
title: Portable network identity
description: When implementing networking-related configuration or telemetry parsing,
  avoid brittle assumptions about IP/host formats and instead use portable defaults
  plus canonical resolution.
repository: Azure/Azure-Sentinel
label: Networking
language: Yaml
comments_count: 3
repository_stars: 6042
---

When implementing networking-related configuration or telemetry parsing, avoid brittle assumptions about IP/host formats and instead use portable defaults plus canonical resolution.

**1) Container/network config: prefer portable defaults**
- Don’t hardcode LAN IPs or make external/dedicated networks mandatory for the default path.
- Use Docker’s default connectivity + explicit `ports:` publishing for out-of-the-box operation.
- If a macvlan/dedicated-IP approach is needed, keep it as an *opt-in* (documented) advanced section.

Example pattern (portable default):
```yaml
services:
  app:
    build: .
    image: myapp:local
    ports:
      - "514:514/udp"
      - "514:514/tcp"
    restart: unless-stopped
# Optional advanced macvlan/dedicated IP configuration goes here as a commented section.
```

**2) Log/parser network identity: preserve and resolve FQDNs**
- Don’t over-restrict hostnames with regexes that invalidate/blank dotted or fully-qualified hostnames.
- Resolve hostnames to canonical values using the approved helper and map to ASIM identity fields (hostname/domain/domain type/FQDN).

Example pattern (canonicalize host identity):
```kusto
| extend
    ResolvedHost = _ASIM_ResolveDvcFQDN('HostName')
| project
    HostName = ResolvedHost.Hostname,
    Domain = ResolvedHost.Domain,
    DomainType = ResolvedHost.DomainType,
    FQDN = ResolvedHost.FQDN
```

Apply this standard to both runtime networking (Compose/Kubernetes) and network identity in parsing so outputs are stable across hosts, DNS styles, and deployment environments.