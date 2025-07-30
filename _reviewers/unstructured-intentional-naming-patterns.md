---
title: intentional naming patterns
description: Recognize when seemingly redundant naming patterns serve specific technical
  purposes rather than being mistakes or oversights. Some naming conventions that
  appear duplicative are actually intentional and necessary for technical reasons.
repository: Unstructured-IO/unstructured
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 12117
---

Recognize when seemingly redundant naming patterns serve specific technical purposes rather than being mistakes or oversights. Some naming conventions that appear duplicative are actually intentional and necessary for technical reasons.

Common examples include:
- Import aliases in type stubs: `from ._element import HtmlElement as HtmlElement` - This pattern avoids unused import errors when republishing imports while maintaining explicit exports
- Function overloads: Multiple functions with identical names but different signatures represent the same logical operation with different interfaces
- Alternative approaches like `__all__ = ["HtmlElement"]` exist but may be less compact or appropriate for the specific context

Before suggesting changes to apparently redundant naming, verify whether the pattern serves a technical requirement such as type checking, import management, or API design. Understanding the underlying purpose helps distinguish between genuine redundancy and intentional technical patterns.

```python
# Intentional - republishing import in type stub
from ._element import HtmlElement as HtmlElement

# Intentional - same logical function, different signatures  
@overload
def strip_elements(tree: _ElementOrTree, tags: Collection[_TagSelector]) -> None: ...
@overload  
def strip_elements(tree: _ElementOrTree, *tags: _TagSelector) -> None: ...
```