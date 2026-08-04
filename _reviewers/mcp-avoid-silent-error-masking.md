---
title: Avoid silent error masking
description: 'Establish a team-wide error-handling contract:


  1) Never swallow exceptions in production paths

  - Avoid bare `except: pass` / broad exception fallbacks that hide the real failure.'
repository: awslabs/mcp
label: Error Handling
language: Python
comments_count: 14
repository_stars: 9545
---

Establish a team-wide error-handling contract:

1) Never swallow exceptions in production paths
- Avoid bare `except: pass` / broad exception fallbacks that hide the real failure.
- If you intentionally swallow (e.g., to preserve a prior/stronger error), add a comment explaining what error you are preserving and why, and always log at least at DEBUG/WARN.

2) Fail closed when safety controls can’t be enforced
- If you set operational safeguards (timeouts, read-only guarantees, pagination caps, etc.), treat enforcement failures as failures.
- Do not continue with “safety bound dropped” behavior.

3) Check both exception paths AND falsy-return failure signals
- Many SDK/driver functions can fail by returning falsy rather than raising. Always verify return values where the API/driver uses falsy to indicate failure.

4) Preserve error meaning in the response contract
- Ensure tools do not return “success-shaped” payloads for errors.
- Use a consistent error payload with an `error_type` (at least `bad_request`, `service_error`, `internal_error`) and include enough context for the agent/ops to recover.
- For partial failures (e.g., some batch calls fail), set explicit flags like `partial_failure=True` and include batch error counts/details.

5) Maintain your own “best-effort” guarantees
- If you claim “best-effort never raises,” ensure you don’t introduce tz/naive-awareness bugs or other issues that can raise unexpectedly.

Minimal implementation pattern:
```python
import json
from typing import Any, Dict


def error_response(message: str, error_type: str) -> str:
    return json.dumps({"error": message, "error_type": error_type})


async def tool_impl(user_input: str) -> Dict[str, Any]:
    try:
        # validate input (bad_request)
        if not user_input:
            return json.loads(error_response("Missing input", "bad_request"))

        # service call
        ok = driver_enforce_timeout(user_input)
        if not ok:  # fail closed on falsy return
            return json.loads(error_response("Could not enforce timeout", "service_error"))

        result = driver_execute(user_input)
        if not result:  # fail closed if falsy indicates failure
            return json.loads(error_response("Execution failed", "service_error"))

        return {"status": "success", "data": result}

    except ValueError as e:
        return json.loads(error_response(str(e), "bad_request"))
    except Exception as e:
        # log exception with traceback in real code
        return json.loads(error_response("Service/internal failure", "internal_error"))
```

Applying this standard will eliminate many recurring review findings: unhandled AWS/driver exceptions ([3]), silent safety-control drops ([4],[5]), lost debug signals ([8],[10]), success-shaped error payloads ([30]), and “best-effort” paths that still raise ([31]).