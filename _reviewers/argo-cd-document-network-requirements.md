---
title: document network requirements
description: When documenting network-dependent features, explicitly specify all network
  configuration requirements including protocol support, certificate handling, and
  infrastructure setup. Users often encounter connectivity issues due to undocumented
  network prerequisites.
repository: argoproj/argo-cd
label: Networking
language: Markdown
comments_count: 4
repository_stars: 20149
---

When documenting network-dependent features, explicitly specify all network configuration requirements including protocol support, certificate handling, and infrastructure setup. Users often encounter connectivity issues due to undocumented network prerequisites.

Include specific configuration examples and verification steps for:
- Required network protocols (e.g., HTTP/2 support)
- TLS certificate handling for self-signed certificates
- Ingress/routing configuration for service endpoints

Example documentation pattern:
```yaml
# Network Requirements
!!! note
    This feature requires HTTP/2 support. Verify your infrastructure supports HTTP/2.

# TLS Configuration (for self-signed certificates)
spec:
  # Skip TLS validation for self-signed certificates
  insecure: true
  # Reference to trusted CA certificates
  caRef:
    configMapName: argocd-tls-certs-cm
    key: azure-devops-ca

# Ingress Configuration
apiVersion: networking.k8s.io/v1
kind: Ingress
spec:
  rules:
    - host: cd.apps.argoproj.io
      http:
        paths:
          - path: /api/webhook
            pathType: Prefix
            backend:
              service:
                name: argocd-applicationset-controller
                port:
                  number: 7000
```

This prevents user frustration from undocumented network dependencies and reduces support burden from connectivity-related issues.