---
title: Add missing code documentation
description: Ensure all methods have docstrings and complex logic includes explanatory
  comments to help contributors understand code intent and functionality. Missing
  documentation creates barriers for new contributors and makes code maintenance more
  difficult.
repository: python-poetry/poetry
label: Documentation
language: Python
comments_count: 2
repository_stars: 33496
---

Ensure all methods have docstrings and complex logic includes explanatory comments to help contributors understand code intent and functionality. Missing documentation creates barriers for new contributors and makes code maintenance more difficult.

For methods, add docstrings that describe the purpose and intended usage:
```python
def _group_by_source(self, deps: list[Dependency]) -> dict[str, list[Dependency]]:
    """Group dependencies by their source origin.
    
    Separates direct origin dependencies from non-direct origin dependencies
    to enable proper constraint merging logic.
    """
```

For complex logic, add comments explaining the reasoning and approach:
```python
# Group dependencies by source to apply different merge strategies
dep_groups = self._group_by_source(deps)
# Merge non-direct dependencies first, then combine with direct ones
# This ensures direct dependencies take precedence in constraint resolution
```

This documentation is especially valuable after refactoring, as it helps reviewers and future maintainers understand the improved logic without having to reverse-engineer the implementation.