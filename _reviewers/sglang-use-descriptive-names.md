---
title: Use descriptive names
description: Choose variable, function, and parameter names that accurately reflect
  their content, type, and purpose. Avoid misleading names that don't match the actual
  data or functionality they represent.
repository: sgl-project/sglang
label: Naming Conventions
language: Python
comments_count: 5
repository_stars: 17245
---

Choose variable, function, and parameter names that accurately reflect their content, type, and purpose. Avoid misleading names that don't match the actual data or functionality they represent.

Key principles:
- Names should clearly indicate what the variable contains or what the function does
- Avoid names that suggest a different type than what's actually stored (e.g., don't use `_list` suffix for non-list variables)
- Use standard, well-understood terminology rather than abbreviations or informal terms
- Balance descriptiveness with conciseness - avoid excessively long names while maintaining clarity

Examples of improvements:
```python
# Misleading - suggests it's a list but contains length
holding_tokens_list = len(tokens)  # Bad

# Clear and accurate
holding_tokens_count = len(tokens)  # Good

# Informal terminology
onfly_info = get_dispatch_info()  # Bad

# Standard terminology  
in_flight_info = get_dispatch_info()  # Good

# Overly verbose
should_fuse_allreduce_residual_rmsnorm = True  # Bad

# Concise but clear
should_allreduce_fusion = True  # Good
```

This practice prevents confusion, reduces debugging time, and makes code more maintainable by ensuring names serve as accurate documentation of the code's intent.