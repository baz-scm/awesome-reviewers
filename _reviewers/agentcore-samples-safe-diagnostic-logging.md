---
title: Safe diagnostic logging
description: "When adding logs or debug output, use them to improve traceability and\
  \ troubleshooting without leaking secrets. \n\n**Do**\n- Log **correlation identifiers**\
  \ (e.g., `session_id`) in a **consistent, known format** (e.g., UUID) so issues\
  \ can be followed end-to-end."
repository: awslabs/agentcore-samples
label: Logging
language: Python
comments_count: 2
repository_stars: 3244
---

When adding logs or debug output, use them to improve traceability and troubleshooting without leaking secrets. 

**Do**
- Log **correlation identifiers** (e.g., `session_id`) in a **consistent, known format** (e.g., UUID) so issues can be followed end-to-end.
- Log **non-sensitive configuration “knobs”** needed to debug behavior (e.g., OAuth **scopes**) so users can quickly spot mismatches.

**Don’t**
- Log **secrets** (passwords, client secrets, tokens, decrypted credentials) or anything that could be used to authenticate.

**Example pattern**
```python
import logging
import uuid

logger = logging.getLogger(__name__)

def log_session_and_scopes(session_id: str, scopes: list[str]):
    # Ensure stable formatting for traceability
    sid = str(uuid.UUID(session_id))  # raises if invalid; consider try/except if needed

    # Log only non-sensitive diagnostics
    logger.info("trace session_id=%s scopes=%s", sid, " ".join(scopes))

# Avoid doing this:
# logger.info("client_secret=%s", client_secret)  # never log secrets
# print("password=...")
```

Apply this across request handlers, scripts, and integration tests: logs should help operators and developers diagnose issues quickly, while keeping authentication material out of outputs.