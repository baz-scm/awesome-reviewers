---
title: Standardize build configurations
description: All components should use consistent build configurations and patterns
  in their CI/CD setup. This includes standardizing Makefile variables, build commands,
  and docker build processes across repositories. Inconsistent build configurations
  make CI/CD pipelines difficult to maintain and can lead to confusion during development.
repository: kubeflow/kubeflow
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 15064
---

All components should use consistent build configurations and patterns in their CI/CD setup. This includes standardizing Makefile variables, build commands, and docker build processes across repositories. Inconsistent build configurations make CI/CD pipelines difficult to maintain and can lead to confusion during development.

For example, use consistent variable naming across Makefiles:
```bash
# Use consistent variable names like REGISTRY_PROJECT
REGISTRY_PROJECT=my-repo make docker-build
```

Instead of having different variable names for the same concept in different components as noted in the discussion:
"Tensorboard's makefile uses slightly different vars but we should iron them out and have the same template"

This standardization simplifies CI/CD pipeline maintenance, improves developer experience when working across components, and ensures that all artifacts follow the same build and testing patterns. It also makes it clearer which components are part of the official CI/CD pipeline and which are provided as examples only.
