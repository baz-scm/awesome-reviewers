---
title: Self-Contained Secure Networking
description: 'Ensure networking-related docs/examples and configurations are both
  runnable and secure: (1) every referenced endpoint/service/backend in an example
  manifest must be defined so the config works when copied, and (2) TLS-related defaults
  (e.g., certificate verification) must default to secure behavior and be treated
  as potentially breaking—clearly...'
repository: apache/apisix
label: Networking
language: Markdown
comments_count: 2
repository_stars: 16922
---

Ensure networking-related docs/examples and configurations are both runnable and secure: (1) every referenced endpoint/service/backend in an example manifest must be defined so the config works when copied, and (2) TLS-related defaults (e.g., certificate verification) must default to secure behavior and be treated as potentially breaking—clearly documented/announced when changing defaults.

Example (Gateway API backend wiring, self-contained):
```yaml
apiVersion: v1
kind: Service
metadata:
  namespace: aic
  name: httpbin-external-domain
spec:
  type: ExternalName
  externalName: httpbin.org
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  namespace: aic
  name: authz-keycloak-route
spec:
  parentRefs:
    - name: apisix
  rules:
    - matches:
        - path:
            type: Exact
            value: /anything
      backendRefs:
        - name: httpbin-external-domain
```

Example (secure TLS verification default, explicit in config):
```yaml
plugins:
  - name: openid-connect
    config:
      ssl_verify: true  # keep secure default; if changing this default, announce as breaking
```

Practical checklist:
- Docs/manifests: verify every `backendRefs.name` (or host) has a corresponding `Service`/DNS target in the same example set.
- Networking security: when TLS verification/scheme defaults change, mark as breaking in changelog and ensure templates/docs show the effective default (`ssl_verify: true`) explicitly.