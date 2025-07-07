---
title: Version AI dependencies appropriately
description: 'When adding or updating dependencies for AI/ML libraries in your project,
  follow these two key practices:


  1. **Set appropriate version constraints** that balance stability with access to
  improvements. For rapidly evolving AI libraries like HuggingFace Hub, avoid overly
  restrictive upper bounds that prevent compatible updates, but also avoid excessively...'
repository: huggingface/tokenizers
label: AI
language: Toml
comments_count: 2
repository_stars: 9868
---

When adding or updating dependencies for AI/ML libraries in your project, follow these two key practices:

1. **Set appropriate version constraints** that balance stability with access to improvements. For rapidly evolving AI libraries like HuggingFace Hub, avoid overly restrictive upper bounds that prevent compatible updates, but also avoid excessively permissive constraints that risk breaking changes.

```toml
# Too restrictive
dependencies = ["huggingface_hub>=0.16.4,<0.17"]

# Better approach - allows minor version updates
dependencies = ["huggingface_hub>=0.16.4,<0.18"]

# Potentially too permissive for rapidly evolving AI libraries
dependencies = ["huggingface_hub>=0.16.4,<1.0"]
```

2. **Make AI-related dependencies optional** when they're not essential for core functionality. This is especially important for dependencies fetched from Git repositories or those with large footprints.

```toml
# Better approach with optional flag
arrow = { git = "https://github.com/apache/arrow-rs", branch = "master", features = [
    "pyarrow",
], optional=True }
```

This approach reduces unnecessary dependencies for users who don't need all ML features and provides flexibility in environments with compatibility constraints.