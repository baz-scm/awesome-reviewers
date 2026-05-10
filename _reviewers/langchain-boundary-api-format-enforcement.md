---
title: Boundary API Format Enforcement
description: When building provider requests or consuming provider responses, enforce
  that all intermediate representations match the provider’s expected wire format
  *at the boundary*—including IDs, message/content blocks, and versioned behavior.
repository: langchain-ai/langchain
label: API
language: Python
comments_count: 8
repository_stars: 136312
---

When building provider requests or consuming provider responses, enforce that all intermediate representations match the provider’s expected wire format *at the boundary*—including IDs, message/content blocks, and versioned behavior.

Practical rules:
1) **Translate/standardize provider-specific formats at payload-construction time** (don’t assume downstream components share the same schema).
   - Example: sanitize provider-enforced IDs before sending (Anthropic tool_use.id regex), and normalize multimodal/message content blocks into the standard format expected by the target path.
2) **Validate provider-required structures immediately before API calls**.
   - Keep validation/normalization in the provider’s formatting/translation layer, not in the base model namespace.
3) **Prevent internal/default flags from leaking into provider payload branching**.
   - Ensure non-streaming codepaths force `stream=False` *before* payload construction, and strip internal-only kwargs so streaming/non-streaming uses the correct branch.
4) **Make API version behavior explicit per invocation** (e.g., `output_version`) and ensure streaming paths filter internal-only fields.

Example (pattern):
```python
def _get_request_payload(messages, *, stream: bool, output_version: str | None, tools=None):
    # 1) validate/translate to wire format
    messages = normalize_messages_for_provider(messages)  # standard blocks/ids
    if tools is not None:
        ensure_tool_schemas_present(tools)  # avoid provider/token-counter failures

    # 2) explicit flags: avoid leakage into branching logic
    kwargs = {"stream": bool(stream)}

    # 3) explicit versioning: don’t rely on defaults
    if output_version is not None:
        kwargs["_output_version"] = output_version

    payload = build_provider_payload(messages, **kwargs)

    # 4) strip internal-only keys so they never reach the provider
    payload.pop("_output_version", None)
    return payload
```
This standard reduces brittle compatibility bugs where the same higher-level object behaves differently depending on hidden flags, streaming vs non-streaming paths, or provider-specific schema requirements.