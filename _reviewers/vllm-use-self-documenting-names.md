---
title: Use self-documenting names
description: Variable, function, and parameter names should accurately reflect their
  purpose, behavior, and content. Choosing descriptive names improves code readability
  and reduces bugs caused by naming confusion.
repository: vllm-project/vllm
label: Naming Conventions
language: Python
comments_count: 6
repository_stars: 51730
---

Variable, function, and parameter names should accurately reflect their purpose, behavior, and content. Choosing descriptive names improves code readability and reduces bugs caused by naming confusion.

When naming variables and parameters:
1. Use names that precisely describe what the entity represents
2. Maintain consistent naming across related components (config parameters, CLI args, classes)
3. Avoid misleading names that imply incorrect functionality or types

Examples of issues to avoid:
```python
# INCORRECT: Using "width" for height is misleading
img_height = image_processor.size.get("width", 224)

# CORRECT: Name accurately reflects the value
img_height = image_processor.size.get("height", 224)

# INCORRECT: CLI flag name doesn't match config parameter
scheduler_group.add_argument("--max-waiting-queue-length", 
                             **scheduler_kwargs["limit_queue_length"])

# CORRECT: Consistent naming between CLI and config
scheduler_group.add_argument("--limit-queue-length", 
                             **scheduler_kwargs["limit_queue_length"])

# INCORRECT: Name in __all__ doesn't match actual class name
__all__ = ["MoEConfig"]  # But actual class is FusedMoEConfig

# CORRECT: Name in __all__ matches the actual implementation
__all__ = ["FusedMoEConfig"]
```

Descriptive and consistent naming serves as implicit documentation, making code more maintainable and reducing the likelihood of errors during development.