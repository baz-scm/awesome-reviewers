---
title: Authenticated health checks
description: When implementing health checks for external services, verify the complete
  communication stack rather than just basic connectivity. Health checks should validate
  that your service can successfully authenticate and perform actual operations, not
  merely establish network connections.
repository: gravitational/teleport
label: Networking
language: Markdown
comments_count: 4
repository_stars: 19109
---

When implementing health checks for external services, verify the complete communication stack rather than just basic connectivity. Health checks should validate that your service can successfully authenticate and perform actual operations, not merely establish network connections.

Basic TCP or TLS connectivity checks only confirm network reachability but miss critical configuration issues like insufficient credentials, improper RBAC setup, or API compatibility problems. Instead, implement health checks that make authenticated requests to meaningful endpoints that exercise the same permissions your service requires during normal operation.

For example, when health checking a Kubernetes cluster, use authenticated API calls like `SelfSubjectAccessReview` to verify proper RBAC configuration:

```go
// Instead of just TCP connectivity
conn, err := net.Dial("tcp", kubernetesEndpoint)

// Use authenticated API calls that verify actual functionality
sarClient := authzapi.NewSelfSubjectAccessReviewInterface(client)
resp, err := sarClient.Create(ctx, &authzapi.SelfSubjectAccessReview{
    Spec: authzapi.SelfSubjectAccessReviewSpec{
        ResourceAttributes: &authzapi.ResourceAttributes{
            Verb:     "get",
            Resource: "pods",
        },
    },
}, metav1.CreateOptions{})
```

This approach catches configuration problems early, such as when "the agent was deployed with insufficient credentials and is unable to talk to the Kubernetes API." It also provides more meaningful health status that reflects whether your service can actually perform its intended operations rather than just reach the target system.

Consider the network characteristics of your health check endpoints - some may be exempt from rate limiting (like Kubernetes `/readyz`) while others may not. Design your health check frequency and retry logic accordingly to avoid overwhelming the target service while still providing timely health status updates.