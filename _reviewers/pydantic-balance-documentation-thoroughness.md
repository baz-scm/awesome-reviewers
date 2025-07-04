---
title: Balance documentation thoroughness
description: 'Documentation should balance completeness with avoiding redundancy.
  When documenting complex features:


  1. Centralize detailed explanations in a single location'
repository: pydantic/pydantic
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 24377
---

Documentation should balance completeness with avoiding redundancy. When documenting complex features:

1. Centralize detailed explanations in a single location
2. Use cross-references and links to connect related concepts
3. Include essential information in overview sections
4. Avoid duplicating content across sections

For example, when documenting multiple related features:

```python
# Good - Using cross-references
"""
Field validation works similarly to [model validation](./models.md#validation).
See the [validation reference](../api/validators.md) for detailed options.
"""

# Avoid - Duplicating detailed explanations
"""
Field validation supports mode='before', mode='after', and mode='wrap'.
The before mode runs before type validation, after mode runs after, etc.
(Repeating all details that are already in the validation reference)
"""
```

This approach makes documentation easier to maintain (changes only need to be made in one place) and helps users find comprehensive information through intuitive navigation. When uncertain whether to include information in multiple places, prefer using links to a canonical source rather than duplicating content.