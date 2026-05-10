---
title: Catch Expected Exceptions
description: When handling failures, avoid broad try/except that hides root causes.
  Catch only the exceptions you expect, log a warning (with enough context to debug),
  and preserve the original error/stack trace. For unsupported/unimplemented functionality
  or dependency/version mismatches, fail explicitly with clear, actionable error messages.
repository: eosphoros-ai/DB-GPT
label: Error Handling
language: Python
comments_count: 5
repository_stars: 18703
---

When handling failures, avoid broad try/except that hides root causes. Catch only the exceptions you expect, log a warning (with enough context to debug), and preserve the original error/stack trace. For unsupported/unimplemented functionality or dependency/version mismatches, fail explicitly with clear, actionable error messages.

Practical rules:
- Prefer: `except SpecificError as e:` over `except Exception:`.
- If you degrade gracefully, log at warning/error level and keep a traceable signal (don’t silently set empty results without context).
- Avoid control-flow patterns that suppress or confuse errors (e.g., returning from a `finally` that runs after an exception).
- For unsupported features: `raise NotImplementedError(...)` (or add a TODO for later), rather than silently passing.
- For dependency problems: detect version capability early and raise an error telling the operator what to upgrade.

Example pattern:
```python
import json
import logging
logger = logging.getLogger(__name__)

async def try_text2gql(text, intent_interpreter, text2cypher, graph_adapter):
    try:
        intention = await intent_interpreter.translate(text)
        interaction = await text2cypher.translate(json.dumps(intention))
        query = interaction.get("query", "")
        if "LIMIT" not in query:
            query += " LIMIT 10"
        return graph_adapter.query(query=query)
    except (KeyError, ValueError) as e:  # expected failures only
        logger.warning("text2gql failed; falling back. text=%r err=%s", text, e)
        return None
```

This keeps behavior predictable, makes production issues diagnosable, and ensures that truly unexpected bugs are not masked.