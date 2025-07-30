---
title: Separate multiple imports
description: When importing multiple items from the same module, use separate import
  statements instead of combining them on a single line. This improves code readability
  and makes it easier to track individual imports during code reviews and refactoring.
repository: smallcloudai/refact
label: Code Style
language: Python
comments_count: 2
repository_stars: 3114
---

When importing multiple items from the same module, use separate import statements instead of combining them on a single line. This improves code readability and makes it easier to track individual imports during code reviews and refactoring.

Instead of:
```python
from refact_webgui.webgui.selfhost_model_resolve import completion_resolve_model, resolve_model_context_size, resolve_tokenizer_name_for_model
```

Use:
```python
from refact_webgui.webgui.selfhost_model_resolve import completion_resolve_model
from refact_webgui.webgui.selfhost_model_resolve import resolve_model_context_size  
from refact_webgui.webgui.selfhost_model_resolve import resolve_tokenizer_name_for_model
```

This approach makes each import explicit, reduces line length, and makes it easier to add, remove, or modify individual imports without affecting others.