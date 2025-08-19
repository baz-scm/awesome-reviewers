---
title: maintain formatting consistency
description: Ensure consistent formatting patterns and styles throughout the codebase,
  both when writing new code and refactoring existing code. When making style improvements
  or refactoring, preserve the original behavior while applying consistent formatting
  standards.
repository: duckdb/duckdb
label: Code Style
language: Python
comments_count: 2
repository_stars: 32061
---

Ensure consistent formatting patterns and styles throughout the codebase, both when writing new code and refactoring existing code. When making style improvements or refactoring, preserve the original behavior while applying consistent formatting standards.

Key principles:
- Use consistent formatting patterns for similar constructs within the same file and across the codebase
- When refactoring code for style improvements, maintain the original algorithm and behavior as closely as possible
- Establish and follow consistent standards for spacing, string formatting, and code structure

Example of inconsistent formatting to avoid:
```python
# Inconsistent f-string spacing and multi-line formatting
print(f"{i}: ", failure_message["benchmark"])  # Note the space after colon
# vs elsewhere in code:
print(f"{i}. ", other_message)  # Note the period and different spacing

# Inconsistent multi-line string formatting
print('''single line approach''')
# vs
print(
    '''
multi-line
approach
'''
)
```

Example of consistent formatting:
```python
# Consistent f-string spacing
print(f"{i}: {failure_message['benchmark']}")
print(f"{j}: {other_message}")

# Consistent multi-line formatting approach
print("""
====================================================
================  FAILURES SUMMARY  ================
====================================================
""")
```

When refactoring substantial portions of code, break changes into separate commits to clearly distinguish between behavioral changes and pure style improvements, making it easier to verify that the original functionality is preserved.