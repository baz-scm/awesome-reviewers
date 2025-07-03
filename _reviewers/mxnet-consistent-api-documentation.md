---
title: Consistent API documentation
description: 'Maintain high-quality, consistent documentation as a critical component
  of API design. Documentation should feature:


  1. Correct grammar and spelling, including proper punctuation and sentence structure'
repository: apache/mxnet
label: API
language: Markdown
comments_count: 2
repository_stars: 20801
---

Maintain high-quality, consistent documentation as a critical component of API design. Documentation should feature:

1. Correct grammar and spelling, including proper punctuation and sentence structure
2. Consistent terminology throughout, especially for parameter names and technical terms
3. Clear explanations of parameter usage and behavior differences

Example:
```python
# GOOD: Clear, consistent documentation with proper terminology
"""
Returns a uniform distribution array.

Parameters:
----------
low : float, optional
    Lower boundary of the output interval. Default is 0.
high : float, optional
    Upper boundary of the output interval. Default is 1.
size : tuple, optional
    Output shape. Default is None.
"""

# BAD: Inconsistent terminology and grammatical errors
"""
Returns uniform distribution array.
Parameters:
----------
low : float, optional
    lower boundary of output interval. Default is 0
high : float, optional
    upper boundary of the output interval. Default is 1
shape : tuple, optional
    Output size. Default is None.
"""
```

Consistent documentation reduces developer confusion and improves API adoption. It serves as the primary interface between your API and its users, making it as important as the implementation itself.
