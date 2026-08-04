---
title: Use Valid API Contracts
description: When calling SDK/toolkit APIs, always adhere to the documented method
  signatures and request/response shapes. Don’t pass guessed or stale keyword arguments,
  and prefer the project’s canonical starter toolkit abstractions for common lifecycle
  operations.
repository: awslabs/agentcore-samples
label: API
language: Other
comments_count: 3
repository_stars: 3244
---

When calling SDK/toolkit APIs, always adhere to the documented method signatures and request/response shapes. Don’t pass guessed or stale keyword arguments, and prefer the project’s canonical starter toolkit abstractions for common lifecycle operations.

**Application**
- **Match the exact parameter name** expected by the client method.
- **Use the correct data structure** (e.g., filter dict shape) required by the API.
- **Prefer official toolkit manager/operations** (e.g., “manager” for creation, “destroy” for cleanup) instead of one-off utilities.

**Example (fixing an API kwarg + payload shape)**
```python
# WRONG: list_events(metadata_filter=...)  # may raise unexpected keyword argument
# RIGHT: list_events(eventMetadata=[...]) with left/operator/right
recommendation_events = customer_session.list_events(
    eventMetadata=[
        {
            "left": {"metadataKey": "interaction_type"},
            "operator": "EQUALS_TO",
            "right": {"metadataValue": {"stringValue": "product_recommendation"}},
        }
    ]
)
```

**Checklist for PRs**
- Verify the call against the SDK/toolkit docs or implementation signature.
- Confirm the request payload schema matches what the API expects (keys, nesting, value types).
- For setup/cleanup, use the toolkit’s provided operations rather than custom helpers.