---
title: Extract Shared Validation
description: 'Prefer small shared helpers for repeated request parsing/validation,
  and use modern, consistent type annotations to keep code readable and uniform.


  Apply this when you see the same “get field → type-check → return error” logic duplicated
  across endpoints or functions.'
repository: infiniflow/ragflow
label: Code Style
language: Python
comments_count: 5
repository_stars: 80174
---

Prefer small shared helpers for repeated request parsing/validation, and use modern, consistent type annotations to keep code readable and uniform.

Apply this when you see the same “get field → type-check → return error” logic duplicated across endpoints or functions.

Example (shared helper with validation):

```py
def _parse_reference_metadata(req: dict):
    extra_body = req.get("extra_body") or {}
    if extra_body and not isinstance(extra_body, dict):
        return get_error_data_result("extra_body must be an object."), False, None

    reference_metadata = extra_body.get("reference_metadata") or {}
    if reference_metadata and not isinstance(reference_metadata, dict):
        return get_error_data_result("reference_metadata must be an object."), False, None

    metadata_fields = reference_metadata.get("fields")
    if metadata_fields is not None and not isinstance(metadata_fields, list):
        return get_error_data_result("reference_metadata.fields must be an array."), False, None

    return None, bool(reference_metadata.get("include", False)), metadata_fields


async def agents_completion_openai_compatibility(tenant_id, agent_id):
    req = await get_request_json()
    err, include_reference_metadata, metadata_fields = _parse_reference_metadata(req)
    if err:
        return err
    # ...use include_reference_metadata/metadata_fields...
```

Style rules to enforce with this approach:
- De-duplicate identical parsing/validation blocks by extracting helpers.
- Keep helpers small and single-purpose; avoid adding too many responsibilities to one function.
- Use modern typing syntax consistently (e.g., `tuple[...]`, `A | B` instead of `Tuple[...]`, `Union[...]`).