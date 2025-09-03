---
title: Safe operations with fallbacks
description: Implement defensive programming by wrapping potentially failing operations
  in safe methods that provide fallback behavior. Critical operations should never
  cause the main functionality to fail due to secondary concerns like formatting,
  logging, or auxiliary processing.
repository: BerriAI/litellm
label: Error Handling
language: Python
comments_count: 4
repository_stars: 28310
---

Implement defensive programming by wrapping potentially failing operations in safe methods that provide fallback behavior. Critical operations should never cause the main functionality to fail due to secondary concerns like formatting, logging, or auxiliary processing.

Key principles:
- Use try-catch blocks around operations that could fail but shouldn't break core functionality
- Provide sensible fallback values when operations fail
- Create helper functions for common failure-prone operations like JSON parsing or data formatting
- Ensure that auxiliary operations (like cost calculation, logging, or formatting) don't prevent the main response from being returned

Example implementation:
```python
# Instead of direct operation that could fail
"x-litellm-response-cost": str(round(response_cost, 6))

# Use safe helper method with fallback
def safe_round_cost(cost: float) -> str:
    try:
        return str(round(cost, 6))
    except Exception:
        return str(cost)  # fallback to original value

"x-litellm-response-cost": safe_round_cost(response_cost)
```

This approach prevents secondary failures from cascading and breaking primary functionality, while still attempting the preferred operation when possible.