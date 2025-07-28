---
title: Specify naming formats explicitly
description: When defining naming conventions in documentation, specifications, or
  APIs, explicitly specify the exact format and patterns to be used. Avoid ambiguous
  descriptions that could lead to inconsistent implementations.
repository: ggml-org/llama.cpp
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 83559
---

When defining naming conventions in documentation, specifications, or APIs, explicitly specify the exact format and patterns to be used. Avoid ambiguous descriptions that could lead to inconsistent implementations.

This prevents confusion about whether to use leading zeros, specific data types, or formatting patterns. Clear specifications ensure all developers implement naming consistently.

Examples of improvement:

Instead of:
```
training.format.version: string (e.g., "1.0") - Specification version
training.tensor.{index} (e.g., training.tensor.0, training.tensor.1, ...)
```

Specify explicitly:
```
training.format.version: uint32 (e.g., 10034 for v1.0.34) - Specification version
training.tensor.{index} (e.g., training.tensor.0, training.tensor.1, ...). No leading zeros.
```

This applies to version numbering schemes, identifier patterns, file naming conventions, and any other naming standards where ambiguity could lead to inconsistent implementation.