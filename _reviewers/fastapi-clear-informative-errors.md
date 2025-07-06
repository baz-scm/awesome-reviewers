---
title: Clear informative errors
description: 'Error messages should be clear, specific, and provide enough context
  to understand the issue without exposing unnecessary implementation details. When
  handling errors:'
repository: fastapi/fastapi
label: Error Handling
language: Python
comments_count: 2
repository_stars: 86871
---

Error messages should be clear, specific, and provide enough context to understand the issue without exposing unnecessary implementation details. When handling errors:

1. Include specific details about what went wrong rather than using generic messages
2. Consider using appropriate attributes of the exception (like `e.msg`) rather than the entire exception
3. For common error cases, provide tailored error messages with appropriate status codes
4. Keep error handling code clean by avoiding unnecessary control structures

**Example - Before:**
```python
except Exception as e:
    http_error = HTTPException(
        status_code=400, detail="There was an error parsing the body"
    )
    
# And with unnecessary else:
if is_multipart_body and has_dict_error:
    raise RequestInvalidContentTypeException(
        status_code=415,
        detail="Unsupported media type: multipart/form-data (expected application/json)",
    )
else:
    raise RequestValidationError(errors, body=body)
```

**Example - After:**
```python
except Exception as e:
    http_error = HTTPException(
        status_code=400, detail=f"There was an error parsing the body: {e.msg}"
    )
    
# Without unnecessary else (since the first raise will exit):
if is_multipart_body and has_dict_error:
    raise RequestInvalidContentTypeException(
        status_code=415,
        detail="Unsupported media type: multipart/form-data (expected application/json)",
    )
raise RequestValidationError(errors, body=body)
```