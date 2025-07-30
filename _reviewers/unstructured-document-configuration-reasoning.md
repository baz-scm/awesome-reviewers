---
title: Document configuration reasoning
description: Always document the reasoning behind configuration decisions, especially
  for temporary settings like dependency pins, parameter choices, and version constraints.
  Include explanations of why the configuration was needed, what problem it solves,
  and when it might be safe to remove or update.
repository: Unstructured-IO/unstructured
label: Configurations
language: Other
comments_count: 4
repository_stars: 12117
---

Always document the reasoning behind configuration decisions, especially for temporary settings like dependency pins, parameter choices, and version constraints. Include explanations of why the configuration was needed, what problem it solves, and when it might be safe to remove or update.

For dependency pins, explain the specific compatibility issue or version conflict being resolved:

```python
# tenacity 9.0.0 is being installed via chroma, but other dependencies (langchain) restrict tenacity
# to <=9.0.0 in other dependency extras and resolve to 8.5.0.
# The original langchain pin: https://github.com/langchain-ai/langchain/pull/849/
tenacity==8.5.0
```

For API parameters, document when parameters conflict or when one supersedes another to avoid confusion. Remove deprecated or conflicting configuration options rather than documenting both. This practice enables future maintainers to understand when temporary configurations can be safely removed and helps prevent accumulation of unnecessary constraints.