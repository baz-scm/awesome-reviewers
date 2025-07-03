---
title: Specific network access documentation
description: When documenting network access methods or service connections, always
  provide specific commands with explicit ports and namespaces rather than general
  approaches. Include clear examples of how to connect to each required service and
  explain the underlying proxying mechanisms.
repository: kubeflow/kubeflow
label: Networking
language: Markdown
comments_count: 3
repository_stars: 15064
---

When documenting network access methods or service connections, always provide specific commands with explicit ports and namespaces rather than general approaches. Include clear examples of how to connect to each required service and explain the underlying proxying mechanisms.

For example, instead of general instructions like:
```
To access the Kubernetes REST API, run kubectl proxy --port=8083.
```

Provide specific commands for each service:
```
To access a Kubernetes service, run `kubectl port-forward -n kubeflow svc/<service-name> <service-proxy-port>:<service-port>` 
e.g. `kubectl port-forward -n kubeflow svc/jupyter-web-app-service 8085:80`.
```

Additionally, document how proxying works and what happens if network connections fail, including any potential cascade effects on dependent services. This specificity helps developers understand exactly what networking configurations are needed and prevents confusion when setting up local development environments or troubleshooting connection issues.
