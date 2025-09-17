---
title: comprehensive test coverage
description: Ensure tests are comprehensive and explicit to prevent regressions and
  gaps in coverage. Tests should cover all scenarios including edge cases, error conditions,
  and boundary conditions. Avoid vague assertions that could pass even when the implementation
  is incorrect.
repository: emcie-co/parlant
label: Testing
language: Python
comments_count: 6
repository_stars: 12205
---

Ensure tests are comprehensive and explicit to prevent regressions and gaps in coverage. Tests should cover all scenarios including edge cases, error conditions, and boundary conditions. Avoid vague assertions that could pass even when the implementation is incorrect.

Key practices:
- Write explicit assertions that verify specific expected outcomes rather than just checking for existence
- Test edge cases and error conditions (empty files, missing parameters, invalid inputs)
- Ensure new functionality includes corresponding tests before merging
- Cover both positive and negative test cases
- Test filtering and boundary logic with multiple data scenarios

Example of explicit vs vague testing:
```python
# Vague - could pass even if no parameters are missing
assert len(missing_params) < max_allowed

# Explicit - tests exact expected behavior  
assert len(missing_params) == 2
assert "required_field" in missing_params
assert "another_field" in missing_params
```

When adding new features or modifying behavior, always ask: "What scenarios could break this?" and "What edge cases am I not testing?" This prevents regressions and ensures robust, reliable code.