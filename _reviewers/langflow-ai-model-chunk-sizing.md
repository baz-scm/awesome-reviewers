---
title: AI model chunk sizing
description: When configuring text processing components that work with AI embedding
  models, proactively consider tokenization limits and chunk size constraints. Many
  embedding models have practical token limits that are lower than their theoretical
  maximums, and text splitting components may not enforce exact chunk sizes.
repository: langflow-ai/langflow
label: AI
language: Other
comments_count: 4
repository_stars: 111046
---

When configuring text processing components that work with AI embedding models, proactively consider tokenization limits and chunk size constraints. Many embedding models have practical token limits that are lower than their theoretical maximums, and text splitting components may not enforce exact chunk sizes.

Always test your chunk size configuration with your specific embedding model to avoid tokenization errors. If you encounter issues, reduce chunk sizes (try 500 tokens or less), adjust overlap settings, or modify separator strategies.

Example configuration considerations:
```
# Split Text component
chunk_size: 500  # Conservative size for embedding models
chunk_overlap: 50  # Reasonable overlap
separator: "\n\n"  # Common separator for consistent splits

# Test with your embedding model
# Inspect component output to verify actual chunk sizes
```

Document any model-specific limitations in your component descriptions and provide fallback strategies. This is especially important for NVIDIA embedding models like `nvidia/nv-embed-v1` and other specialized AI models that may have stricter practical limits than advertised.