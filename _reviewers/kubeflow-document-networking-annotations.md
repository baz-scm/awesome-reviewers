---
title: Document networking annotations
description: When using Istio or other networking-related annotations in configuration
  files, always include detailed comments explaining their purpose, behavior, and
  effects. This makes networking constraints and logic transparent to developers and
  users who need to understand the system's behavior.
repository: kubeflow/kubeflow
label: Networking
language: Yaml
comments_count: 2
repository_stars: 15064
---

When using Istio or other networking-related annotations in configuration files, always include detailed comments explaining their purpose, behavior, and effects. This makes networking constraints and logic transparent to developers and users who need to understand the system's behavior.

For each networking annotation:
1. Document what the annotation does
2. Explain when/why it's applied
3. Note any specific paths or headers affected

Example:
```yaml
imageGroupOne:
  # The annotation `notebooks.kubeflow.org/http-rewrite-uri: /`
  # is applied to notebook in this group, configuring
  # the Istio rewrite for containers that host their web UI at `/`
  value: public.ecr.aws/j1r0q0g6/notebooks/notebook-servers/codeserver-python:master-1831e436

imageGroupTwo:
  # The annotation `notebooks.kubeflow.org/http-rewrite-uri: /`
  # is applied to notebook in this group, configuring
  # the Istio rewrite for containers that host their web UI at `/`
  # The annotation `notebooks.kubeflow.org/http-headers-request-set`
  # is applied to notebook in this group, configuring Istio
  # to add the `X-RStudio-Root-Path` header to requests
  value: public.ecr.aws/j1r0q0g6/notebooks/notebook-servers/rstudio:master-1831e436
```

This practice ensures that network routing behaviors are explicit, making the system more maintainable and reducing confusion when debugging networking issues.
