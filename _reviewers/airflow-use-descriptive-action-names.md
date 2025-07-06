---
title: Use descriptive action names
description: Names should clearly indicate purpose and behavior using appropriate
  action verbs and descriptive terms. This applies to functions, methods, variables,
  and classes. Avoid generic or ambiguous names that don't convey the actual functionality.
repository: apache/airflow
label: Naming Conventions
language: Python
comments_count: 8
repository_stars: 40858
---

Names should clearly indicate purpose and behavior using appropriate action verbs and descriptive terms. This applies to functions, methods, variables, and classes. Avoid generic or ambiguous names that don't convey the actual functionality.

Key guidelines:
1. Use verb-based names for functions/methods that describe the action
2. Choose class names that reflect their primary purpose
3. Avoid shadowing names from imports or parent scopes
4. Keep related name patterns consistent

Example of good naming:
```python
# Better names that clearly indicate purpose
def sync_to_local_dir(self, bucket_name: str):  # vs generic "download_s3"
def add_debug_span(func):  # vs ambiguous "add_span" 

# Consistent naming pattern for related properties
class ViewResponse(BaseModel):
    icon: str | None = None
    icon_dark_mode: str | None = None  # vs disconnected "dark_mode_icon"

# Avoid shadowing in loops
for progress_line in progress_callback_lines:  # vs reusing "line"
    process(progress_line)
```