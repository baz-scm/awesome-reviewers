---
title: Restrict database access
description: Never allow unrestricted public access (0.0.0.0/0) to database instances.
  Restrict database network access to only specific trusted IP ranges or VPC networks
  that require it, following the principle of least privilege. This prevents potential
  unauthorized access and data breaches.
repository: n8n-io/n8n
label: Security
language: Terraform
comments_count: 1
repository_stars: 122978
---

Never allow unrestricted public access (0.0.0.0/0) to database instances. Restrict database network access to only specific trusted IP ranges or VPC networks that require it, following the principle of least privilege. This prevents potential unauthorized access and data breaches.

Example of problematic configuration:
```terraform
postgres_authorized_networks = [
  {
    name  = "all"
    value = "0.0.0.0/0"
  }
]
```

Example of improved configuration:
```terraform
postgres_authorized_networks = [
  {
    name  = "internal-network"
    value = "10.0.0.0/8"
  },
  {
    name  = "office-network"
    value = "203.0.113.0/24"
  }
]
```