---
title: Document migration paths
description: 'When implementing version changes or migrations, provide comprehensive
  documentation and tools to support users through the transition process. This includes:'
repository: kubeflow/kubeflow
label: Migrations
language: Markdown
comments_count: 2
repository_stars: 15064
---

When implementing version changes or migrations, provide comprehensive documentation and tools to support users through the transition process. This includes:

1. Clearly identify and document breaking changes between versions
2. List specific dependencies required before and after migration
3. Provide step-by-step upgrade instructions with realistic expectations
4. Create migration tools with concrete usage examples

For example, when creating a version converter tool:

```
# KfDef version converter

## Overview
This is a simple helper CLI that converts KfDef between versions.

## Usage
A simple CLI to convert KfDef from v1alpha1 to v1beta1

Usage:
  kfdef-converter [command]

Available Commands:
  help        Help about any command
  tov1beta1   Convert a KfDef config in v1alpha1 into v1beta1 format.

## Example
# Convert a config file from v1alpha1 to v1beta1
kfdef-converter tov1beta1 --input=/path/to/old-config.yaml --output=/path/to/new-config.yaml
```

When planning roadmaps that include migrations, be specific about upgrade capabilities rather than making general promises. If complete migration support isn't feasible, consider defining limited scope migrations or marking them as stretch goals.
