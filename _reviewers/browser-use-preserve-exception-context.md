---
title: preserve exception context
description: 'When handling exceptions, always preserve the original error context
  to aid in debugging and error diagnosis. This involves two key practices: (1) Include
  the exception class name when converting exceptions to strings, and (2) Use exception
  chaining when re-raising exceptions.'
repository: browser-use/browser-use
label: Error Handling
language: Python
comments_count: 2
repository_stars: 69139
---

When handling exceptions, always preserve the original error context to aid in debugging and error diagnosis. This involves two key practices: (1) Include the exception class name when converting exceptions to strings, and (2) Use exception chaining when re-raising exceptions.

For error message formatting, avoid bare `str(e)` or `f'{e}'` as these only show the error message without the exception type. Instead, use `f'{type(e).__name__}: {e}'` to include both the exception class and message.

When re-raising exceptions or wrapping them in custom exceptions, always preserve the original traceback using `from e` to maintain the full error context for debugging.

Example of proper exception context preservation:

```python
try:
    response: dict[str, Any] = await structured_llm.ainvoke(input_messages)
    parsed: AgentOutput | None = response['parsed']
except Exception as e:
    logger.error(f'Failed to invoke model: {type(e).__name__}: {e}')
    raise LLMException(401, 'LLM API call failed') from e

# For error reporting in return values:
except Exception as e:
    return {
        'task_id': task_folder.name, 
        'judgement': None, 
        'success': False, 
        'error': f'{type(e).__name__}: {e}', 
        'score': 0.0
    }
```

This practice significantly improves error diagnosis by providing complete context about what went wrong and where the error originated, making debugging much more efficient.