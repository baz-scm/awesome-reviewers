---
title: Maintainable documentation hygiene
description: 'Documentation should be kept authoritative and maintainable: use stable
  links, avoid recommending deprecated APIs, and remove misleading/ineffective documentation
  details.'
repository: langchain-ai/langchain
label: Documentation
language: Other
comments_count: 3
repository_stars: 136312
---

Documentation should be kept authoritative and maintainable: use stable links, avoid recommending deprecated APIs, and remove misleading/ineffective documentation details.

Apply it as follows:
- Prefer stable/canonical URLs (often relative) for “view tutorial” links; don’t pin to a specific external commit hash.
- Keep examples focused on the intended surface area. If documenting a tool, show tool usage (e.g., `tool.invoke(...)`) rather than agent-creation workflows.
- Remove or avoid examples of deprecated functionality.
- Don’t document schema/config values that are ineffective for the given type (e.g., an array `default` that provides no value in JSON Schema).

Example (tool-only, non-deprecated usage):
```python
from langchain_desearch.tools import DesearchTool

tool = DesearchTool()
result = tool.invoke({"query": "LLM RAG best practices"})
print(result)
```