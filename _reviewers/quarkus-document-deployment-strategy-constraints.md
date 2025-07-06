---
title: Document deployment strategy constraints
description: Always document and enforce appropriate deployment strategies for different
  application types in your CI/CD pipeline configuration. Different deployment strategies
  have specific constraints that must be considered for successful application delivery.
repository: quarkusio/quarkus
label: CI/CD
language: Other
comments_count: 3
repository_stars: 14667
---

Always document and enforce appropriate deployment strategies for different application types in your CI/CD pipeline configuration. Different deployment strategies have specific constraints that must be considered for successful application delivery.

For example, when deploying Quarkus applications:
- Use Docker build strategy for native executable deployments to OpenShift
- S2I (Source-to-Image) can be used for JVM-based deployments, but is not suitable for native deployments
- Binary builds are appropriate for simpler deployment scenarios

Include clear configuration examples in your CI/CD documentation:

```properties
# For native application deployment using Docker build strategy
quarkus.openshift.build-strategy=docker
quarkus.native.container-build=true

# Optional: Container runtime specification
quarkus.native.container-runtime=docker  # or podman

# Additional configuration for your environment
quarkus.kubernetes-client.trust-certs=true
quarkus.openshift.route.expose=true
```

Ensure your pipeline documentation explains the implications of each strategy, including customization options, security considerations, and verification steps appropriate for each deployment approach.