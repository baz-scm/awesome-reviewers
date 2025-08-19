---
title: Python syntax consistency
description: Ensure Python code follows proper naming conventions and syntax rules.
  Use snake_case for variable and parameter names instead of camelCase, and use capitalized
  boolean literals (True/False) instead of lowercase variants from other languages.
repository: microsoft/playwright
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 76113
---

Ensure Python code follows proper naming conventions and syntax rules. Use snake_case for variable and parameter names instead of camelCase, and use capitalized boolean literals (True/False) instead of lowercase variants from other languages.

This addresses common issues when adapting code examples from other languages or when developers switch between different programming contexts. Both naming and boolean literal consistency are essential for Python code correctness and readability.

Example:
```python
# Incorrect
context = await browser.new_context(
  isMobile=false
)

# Correct  
context = await browser.new_context(
  is_mobile=False
)
```