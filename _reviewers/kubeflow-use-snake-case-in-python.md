---
title: Use snake_case in Python
description: Follow Python's PEP 8 naming convention by using snake_case for variables,
  functions, and methods rather than camelCase or other styles. This enhances readability
  and maintains consistency across the codebase.
repository: kubeflow/kubeflow
label: Naming Conventions
language: Python
comments_count: 3
repository_stars: 15064
---

Follow Python's PEP 8 naming convention by using snake_case for variables, functions, and methods rather than camelCase or other styles. This enhances readability and maintains consistency across the codebase.

According to [PEP 8](https://peps.python.org/pep-0008/#descriptive-naming-styles), variable and function names in Python should use lowercase with words separated by underscores (snake_case).

**Instead of writing:**
```python
def set_notebook_memory(notebook, body, defaults):
    container = notebook["spec"]["template"]["spec"]["containers"][0]
    
    memory = get_form_value(body, defaults, "memory")
    memoryLimit = get_form_value(body, defaults, "memoryLimit")
```

**Write:**
```python
def set_notebook_memory(notebook, body, defaults):
    container = notebook["spec"]["template"]["spec"]["containers"][0]
    
    memory = get_form_value(body, defaults, "memory")
    memory_limit = get_form_value(body, defaults, "memoryLimit")
```

This applies to all variable names, function names, method names, and module names in Python code. Class names should use CapWords (PascalCase) convention.
