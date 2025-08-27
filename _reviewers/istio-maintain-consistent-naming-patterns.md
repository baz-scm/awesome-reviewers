---
title: maintain consistent naming patterns
description: Ensure naming consistency across related components and throughout the
  codebase to prevent developer confusion and maintenance issues. When similar concepts
  use different naming variations, choose one pattern and apply it consistently.
repository: istio/istio
label: Naming Conventions
language: Yaml
comments_count: 3
repository_stars: 37192
---

Ensure naming consistency across related components and throughout the codebase to prevent developer confusion and maintenance issues. When similar concepts use different naming variations, choose one pattern and apply it consistently.

Key principles:
- Avoid similar but different names within the same context (e.g., "serve" vs "server")
- Prefer global consistency over local alignment when naming conflicts arise
- Establish systematic patterns for recurring naming decisions (like Kubernetes labels)

Example from the codebase:
```yaml
# Inconsistent - causes confusion
metadata:
  name: mtls-serve  # directory uses "serve"
spec:
  containers:
    - name: mtls-serve
      image: localhost:5000/mtls-server:latest  # image uses "server"

# Consistent - clear and predictable
metadata:
  name: mtls-server
spec:
  containers:
    - name: mtls-server
      image: localhost:5000/mtls-server:latest
```

When updating legacy naming, prioritize consistency with the broader system over maintaining alignment with individual objects. This reduces cognitive load and prevents the type of confusion that "is going to trip someone up one day."