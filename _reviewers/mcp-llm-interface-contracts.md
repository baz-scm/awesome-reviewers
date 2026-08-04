---
title: LLM Interface Contracts
description: 'When exposing APIs/tools to an LLM, treat docstrings, parameter semantics,
  and output size as an interface contract: make it unambiguous, match callable tool
  names exactly, structure “what to do” for reliable parsing, and cap context/token
  growth.'
repository: awslabs/mcp
label: AI
language: Python
comments_count: 6
repository_stars: 9545
---

When exposing APIs/tools to an LLM, treat docstrings, parameter semantics, and output size as an interface contract: make it unambiguous, match callable tool names exactly, structure “what to do” for reliable parsing, and cap context/token growth.

Apply these rules:
1) Guidance must match the callable surface
   - Ensure any LLM-visible text (tool descriptions, doc cross-references, runtime next_step strings) uses the *exact registered tool names*, not internal function names.
2) Make parameter meaning explicit (especially for similar/overlapping filters)
   - If multiple parameters can select similar subsets, spell out the differences in tool descriptions so the LLM can choose the correct one.
3) Use structured discovery text for dispatcher-style tools
   - For single-tool dispatchers (e.g., `action` param), represent the action→required-parameters mapping in a compact, JSON-like block inside the docstring.
4) Keep model/schema field descriptions minimal
   - Avoid duplicating instructions inside model field descriptions; keep instructions in the tool/server layer.
5) Enforce token/context-safe defaults
   - Default query/result limits should be conservative; large payloads must be opt-in.
   - Truncate or “link out” very long strings that otherwise explode context (e.g., long commands/instructions), unless the client explicitly requests full detail.

Example (structured dispatcher + parameter contract):
```python
def rum(action: str, page_url: str | None = None, **kwargs) -> str:
    """CloudWatch RUM tools.

    Actions:
    {
      "errors": {"required": [], "optional": ["page_url", "group_by"]},
      "performance_navigation": {"required": [], "optional": ["page_url"]}
    }

    Parameter semantics:
    - page_url: if provided, filters by metadata.pageId.

    Notes:
    - session_detail defaults to limit=100; pass a higher `limit` only if you need full replay.
    """
    ...
```

Example (token-safe default limit):
```python
def session_detail_query(session_id: str, limit: int = 100) -> str:
    return f"""fields @timestamp, event_type, metadata.pageId, event_details.duration
| filter user_details.sessionId = "{session_id}"
| sort @timestamp asc
| limit {limit}"""
```