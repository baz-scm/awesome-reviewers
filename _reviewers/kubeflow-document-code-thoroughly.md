---
title: Document code thoroughly
description: 'Always include appropriate documentation in your code to improve readability,
  maintainability, and usability:


  1. **Document all public APIs** with Go doc comments:'
repository: kubeflow/kubeflow
label: Documentation
language: Go
comments_count: 4
repository_stars: 15064
---

Always include appropriate documentation in your code to improve readability, maintainability, and usability:

1. **Document all public APIs** with Go doc comments:
   ```go
   // MetricsExporter provides functionality for exporting metrics to Prometheus
   // and managing metrics collection within the application.
   type MetricsExporter struct {
       // fields...
   }
   
   // IncRequestCounter increments the request counter for the specified kind.
   // It tracks API usage patterns for monitoring purposes.
   func IncRequestCounter(kind string) {
       // implementation...
   }
   ```

2. **Explain complex logic** with inline comments, especially when there are relationships between components or non-obvious behaviors:
   ```go
   // Update the CR status based on the ContainerState of the container
   // that has the same name as the CR
   if len(pod.Status.ContainerStatuses) > 0 {
       // implementation...
   }
   ```

3. **Document code modifications** by adding TODOs with context for commented-out or temporary code:
   ```go
   // TODO(user): This endpoint is temporarily disabled until issue #123 is resolved
   // which addresses the race condition in the deployment creation process.
   //
   //// GetLatestKfdef returns latest kfdef status.
   ```

Following these practices ensures code is understandable to new team members, facilitates easier maintenance, and helps API consumers use your code correctly. Run tools like `go vet ./...` regularly to catch missing documentation on public elements.
