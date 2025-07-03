---
title: Complete documented references
description: 'PyTorch documentation should be comprehensive and include proper cross-references
  to related content. This means:


  1. Including step-by-step instructions for tools and features'
repository: pytorch/pytorch
label: Pytorch
language: Markdown
comments_count: 2
repository_stars: 91169
---

PyTorch documentation should be comprehensive and include proper cross-references to related content. This means:

1. Including step-by-step instructions for tools and features
2. Using proper cross-reference formatting (`{ref}`) to link related documentation
3. Providing clear guidance for common use cases

For example, when documenting analysis tools:
```markdown
# `torch._inductor.analysis`
Contains scripts for inductor performance analysis.

## Usage
1. Profile capture: [steps for capturing profiles]
2. Profile augmenting: [steps for augmenting profiles]
3. Profile comparison: [steps for comparing profiles]
```

When referencing other sections in documentation, use proper cross-reference syntax:
```markdown
The schema for built-in functions like `aten::zeros` can be found at {ref}`builtin functions`.
```

This helps users navigate through PyTorch's extensive documentation and find relevant information quickly, which is essential for effectively using the framework's complex features and tools.
