---
title: Use descriptive names
description: Choose names that clearly describe the purpose, behavior, or content
  of variables, methods, and classes. Avoid ambiguous or generic names that require
  additional context to understand.
repository: langgenius/dify
label: Naming Conventions
language: Python
comments_count: 10
repository_stars: 114231
---

Choose names that clearly describe the purpose, behavior, or content of variables, methods, and classes. Avoid ambiguous or generic names that require additional context to understand.

Key principles:
- Include units or context in names when relevant (e.g., `timeout_seconds` instead of `timeout`)
- Use descriptive verbs for methods that indicate their action (e.g., `create_or_update` instead of `create_alias`)
- Specify the role or relationship in parameter names (e.g., `_creator_user_id` instead of `_created_by`)
- Use plural forms for collections to avoid ambiguity (e.g., `doc_ids` instead of `doc_id`)
- Choose method names that accurately reflect their behavior (e.g., `preserve_flask_contexts` instead of `flask_context_manager`)

Examples of improvements:
```python
# Before: Ambiguous naming
def create_alias(user, timeout):
    doc_id = set()

# After: Descriptive naming  
def create_or_update_alias(creator_user_id, timeout_seconds):
    doc_ids = set()
```

This practice makes code self-documenting and reduces the cognitive load for developers reading and maintaining the codebase.