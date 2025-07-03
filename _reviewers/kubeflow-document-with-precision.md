---
title: Document with precision
description: 'Write informative, consistent, and precise code comments throughout
  your codebase. When documenting code:


  1. **Be specific with references** - When referencing external repositories or sources,
  link to specific versions and files, not just directories. Use precise language
  to describe the relationship between your code and external sources.'
repository: kubeflow/kubeflow
label: Documentation
language: Dockerfile
comments_count: 3
repository_stars: 15064
---

Write informative, consistent, and precise code comments throughout your codebase. When documenting code:

1. **Be specific with references** - When referencing external repositories or sources, link to specific versions and files, not just directories. Use precise language to describe the relationship between your code and external sources.

```
# AVOID:
# Content below is extracted from scripts/Dockerfiles here:
# https://github.com/HabanaAI/Setup_and_Install/tree/main/dockerfiles/base

# BETTER:
# Content below is based on:
# https://github.com/HabanaAI/Setup_and_Install/blob/1.17.0/dockerfiles/base/Dockerfile.ubuntu22.04
```

2. **Add explanatory comments** - Include brief descriptions for significant code blocks, especially when installing components or defining important configurations.

```
# AVOID:
RUN python3 -m pip install habana_media_loader=="${VERSION}"."${REVISION}"

# BETTER:
# Install Habana media loader library for PyTorch integration
RUN python3 -m pip install habana_media_loader=="${VERSION}"."${REVISION}"
```

3. **Maintain consistent styles** - Use consistent comment headers and styles across similar files to improve readability and maintainability.

```
# AVOID mixing styles:
# version details
# and elsewhere:
# args - software versions

# BETTER: Use consistent headers:
# args - software versions
```

Well-documented code improves comprehension, facilitates maintenance, and enhances collaboration among team members.
