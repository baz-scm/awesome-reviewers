---
title: Fail securely by default
description: When designing systems that handle sensitive operations, always default
  to the most secure behavior rather than prioritizing convenience. This practice
  applies to error handling, execution environments, and security-critical fallbacks.
repository: crewaiinc/crewai
label: Security
language: Python
comments_count: 2
repository_stars: 33945
---

When designing systems that handle sensitive operations, always default to the most secure behavior rather than prioritizing convenience. This practice applies to error handling, execution environments, and security-critical fallbacks.

Key principles to follow:

1. **Sanitize error responses**: Never expose internal exception details or stack traces in API responses that could reveal implementation details to potential attackers.

2. **Require explicit opt-in for reduced security**: Don't silently fall back to less secure modes of operation; require explicit configuration through environment variables or parameters.

3. **Log security-relevant decisions**: Ensure security-related fallbacks are clearly logged for monitoring and debugging.

Example of insecure error handling:
```python
except Exception as e:
    return JSONResponse(
        content=JSONRPCResponse(
            id=request_id,
            error=InternalError(data=str(e)),  # Exposes potentially sensitive details
        ),
        status_code=500,
    )
```

Secure implementation:
```python
except Exception as e:
    # Log complete details for internal use
    self.logger.exception(f"Error handling {method} request")
    # Return sanitized response to external users
    return JSONResponse(
        content=JSONRPCResponse(
            id=request_id,
            error=InternalError(data="An internal server error occurred"),
        ),
        status_code=500,
    )
```

Example of insecure fallback:
```python
unsafe_mode = not self.check_docker_available()
# Silently proceeds with unsafe execution
```

Secure implementation:
```python
if not self.check_docker_available():
    if os.getenv("CREWAI_GUARDRAIL_EXECUTION_MODE") == "allow_unsafe":
        self.logger.warning("Docker unavailable. Falling back to unsafe execution mode.")
        self.unsafe_mode = True
    else:
        raise SecurityError("Cannot execute code safely. Docker unavailable and unsafe execution not explicitly enabled.")
```