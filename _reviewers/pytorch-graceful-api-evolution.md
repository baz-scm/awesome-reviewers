---
title: Graceful API evolution
description: 'When modifying, deprecating, or replacing APIs, ensure a smooth transition
  experience for developers by following these practices:


  1. **Add deprecation warnings** when removing or changing public APIs to alert users:'
repository: pytorch/pytorch
label: API
language: Python
comments_count: 6
repository_stars: 91345
---

When modifying, deprecating, or replacing APIs, ensure a smooth transition experience for developers by following these practices:

1. **Add deprecation warnings** when removing or changing public APIs to alert users:
   ```python
   @deprecated(
       "`isinstance(treespec, LeafSpec)` is deprecated, "
       "use `isinstance(treespec, TreeSpec)` and `treespec.is_leaf()` instead.",
       category=FutureWarning,
   )
   class LeafSpec(TreeSpec):
       # ...
   ```

2. **Provide clear migration paths** in deprecation messages and documentation that show exactly how to transition from old APIs to new ones.

3. **Manage public exports** by updating `__all__` lists to remove deprecated items, preventing new code from adopting soon-to-be-removed APIs.

4. **Ensure interoperability** between old and new implementations during transition periods, allowing gradual migration without breaking existing code.

5. **Consider API surface area** when making changes - private APIs may change more freely, while public APIs require more careful transition planning.

Following these practices helps maintain trust with developers using your libraries and reduces friction during necessary API evolution.