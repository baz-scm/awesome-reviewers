---
title: AI model documentation consistency
description: Ensure consistent parameter names and configuration instructions across
  AI model documentation. Inconsistent documentation about model parsers, parameters,
  and configuration options leads to developer confusion and implementation errors.
repository: sgl-project/sglang
label: AI
language: Other
comments_count: 2
repository_stars: 17245
---

Ensure consistent parameter names and configuration instructions across AI model documentation. Inconsistent documentation about model parsers, parameters, and configuration options leads to developer confusion and implementation errors.

When documenting AI model configuration options, maintain consistency in:
- Parameter names and formats (e.g., `qwen3-thinking` vs `qwen3/qwen3-thinking`)
- Usage instructions and examples
- Supported configuration combinations

Example of inconsistent documentation to avoid:
```
# In one place:
Use `--reasoning-parser qwen3/qwen3-thinking`

# In another place:
Use `--reasoning-parser qwen3-thinking` or `--reasoning-parser qwen3`
```

Instead, establish and follow a single standard format across all documentation, clearly specifying which parsers work with which model types and their exact parameter syntax.