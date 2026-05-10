---
title: Preserve API Contracts
description: 'When transforming data to/from the API, always implement the backend’s
  explicit contract: ordering invariants, exact serialization, correct parsing by
  response format/content-type, endpoint-appropriate headers, and backend-specific
  URL/auth/version rules.'
repository: openai/openai-python
label: API
language: Python
comments_count: 9
repository_stars: 30731
---

When transforming data to/from the API, always implement the backend’s explicit contract: ordering invariants, exact serialization, correct parsing by response format/content-type, endpoint-appropriate headers, and backend-specific URL/auth/version rules.

Apply these checks consistently:
- **Response → Request transformations:** preserve required item ordering/pairing invariants (don’t filter/reorder reasoning items).
- **Serialization:** ensure request payloads don’t leak SDK-only/internal fields; use the model’s API-specific exclude behavior.
- **Response parsing:** parse JSON only when the response is JSON (or the selected response_format implies JSON); otherwise treat as plain text/SRT/VTT.
- **Headers per endpoint:** rely on SDK/client-managed auth headers for every endpoint; don’t override headers that are incompatible with a specific transport (e.g., streaming/cancel).
- **Backend differences (Azure/OpenAI):** generate the correct URL path/query and set auth header keys based on `api_type`.
- **LRO/polling:** use correct terminal-state checks and keep polling logic close to the owning resource.

Example (response-format-safe parsing + invariant-preserving payload building):
```py
def get_response_input_items(response):
    # preserve required reasoning->assistant consecutive pairing
    items = []
    for output_item in response.output:
        items.append(output_item.model_dump(exclude_unset=True))
    return items

def parse_response(rbody: str, headers: dict[str,str], response_format):
    if response_format == "json" or headers.get("Content-Type") == "application/json":
        return json.loads(rbody)
    return rbody  # text/srt/vtt
```

Rule of thumb: if the contract can be stated as “must be ordered X”, “must be JSON vs text Y”, or “must send header key Z / URL path P”, encode it as logic + validation—not as an assumption.