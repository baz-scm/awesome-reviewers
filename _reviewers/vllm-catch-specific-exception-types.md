---
title: Catch specific exception types
description: 'Avoid using broad exception handlers like `except Exception:` or bare
  `except:`. Instead, catch specific exception types that you expect and can handle
  meaningfully. This makes code more maintainable by:'
repository: vllm-project/vllm
label: Error Handling
language: Python
comments_count: 8
repository_stars: 51730
---

Avoid using broad exception handlers like `except Exception:` or bare `except:`. Instead, catch specific exception types that you expect and can handle meaningfully. This makes code more maintainable by:
1. Preventing bugs from being silently masked
2. Making error handling intentions clear
3. Improving debugging by preserving stack traces

Example:

```python
# Bad - catches and hides all errors
try:
    result = json.loads(args.compilation_config)
except Exception as e:
    logger.error(f"Error: {e}")
    return None

# Good - handles specific expected error
try:
    result = json.loads(args.compilation_config)
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON configuration: {e}")
    raise ValueError(f"Configuration must be valid JSON: {e}") from e
```

When catching multiple exceptions, order them from most specific to most general. If you must catch a broad exception (e.g., for API boundaries), log the full exception details and consider re-raising or wrapping in a domain-specific error.