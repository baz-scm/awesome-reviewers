---
title: Notebook dependency install
description: When authoring AI/LLM tutorials in Jupyter notebooks, ensure dependency
  installation is done with correct notebook syntax and that nearby explanatory text
  is unambiguous.
repository: langchain-ai/langchain
label: AI
language: Other
comments_count: 2
repository_stars: 136312
---

When authoring AI/LLM tutorials in Jupyter notebooks, ensure dependency installation is done with correct notebook syntax and that nearby explanatory text is unambiguous.

- Use Jupyter magics for installs inside cells (not commented shell commands or bare `pip` lines).
- Keep documentation wording precise when describing session/message history behavior.

Example:
```python
# In a notebook cell (ipynb), use the magic:
%pip install langchain_community

# And keep narrative wording clear when describing state:
# "...wraps the model and adds to this message history..."
```