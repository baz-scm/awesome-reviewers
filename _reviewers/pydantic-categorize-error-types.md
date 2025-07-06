---
title: Categorize error types
description: 'Distinguish between different categories of errors and handle each appropriately.
  Specifically:


  1. **Validation errors** occur during normal operation when input data doesn''t
  match expectations. These should be caught and handled gracefully.'
repository: pydantic/pydantic
label: Error Handling
language: Markdown
comments_count: 3
repository_stars: 24377
---

Distinguish between different categories of errors and handle each appropriately. Specifically:

1. **Validation errors** occur during normal operation when input data doesn't match expectations. These should be caught and handled gracefully.
2. **Usage errors** indicate developer mistakes in using your API and generally shouldn't be caught.

Document these distinctions clearly for API users and provide correct alternatives for common error scenarios.

```python
# BAD: Catching usage errors that indicate developer mistakes
try:
    # Code that might produce both validation and usage errors
    result = model(invalid_input)
except Exception:  # Too broad!
    log_error("An error occurred")
    
# GOOD: Only catch expected validation errors
try:
    result = model(user_input)
except ValidationError as e:
    # Handle validation errors gracefully
    log_error(f"Validation failed: {e}")
    show_user_friendly_message()
    
# Usage errors (like PydanticUserError) aren't caught,
# allowing them to crash during development when they can be fixed

# In documentation, clearly explain error categories:
"""
## Error Types

### Validation Errors
Errors that happen during data validation when user input doesn't match schema.
These can be caught and handled at runtime.

### Usage Errors 
Errors that happen when using the API incorrectly.
These indicate developer mistakes and shouldn't be caught.
"""
```