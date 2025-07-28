---
title: Maintain consistent naming patterns
description: Follow established naming conventions in the codebase and align with
  original source patterns while using modern, non-deprecated alternatives. Avoid
  creating confusing duplication in naming structures.
repository: ggml-org/llama.cpp
label: Naming Conventions
language: Python
comments_count: 3
repository_stars: 83559
---

Follow established naming conventions in the codebase and align with original source patterns while using modern, non-deprecated alternatives. Avoid creating confusing duplication in naming structures.

When adding new components, maintain consistency with existing patterns rather than creating new naming schemes. For example, if existing tensors use `blk.{bid}.component` format, continue that pattern rather than introducing `component.{bid}.component` which creates duplication.

Use modern language features and avoid deprecated imports. Replace deprecated typing constructs like `Dict` with built-in alternatives like `dict` or more appropriate types like `Mapping`.

When naming classes or components based on external models, align with the original naming conventions including version suffixes to maintain traceability and consistency.

Example:
```python
# Good: Consistent with existing pattern, avoids duplication
MODEL_TENSOR.SHORTCONV_CONV: "blk.{bid}.shortconv.conv"

# Avoid: Creates confusing duplication
MODEL_TENSOR.SHORTCONV_CONV: "shortconv.{bid}.shortconv.conv"

# Good: Modern typing
from typing import Callable, Iterator, dict

# Avoid: Deprecated typing
from typing import Dict
```