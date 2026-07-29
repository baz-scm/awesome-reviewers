---
title: Wire Contract Enforcement
description: 'External API boundaries must enforce the *final wire contract*: only
  supported parameters, only provider-accepted content shapes, and only schema-valid
  payloads.'
repository: nousresearch/hermes-agent
label: API
language: Python
comments_count: 7
repository_stars: 221948
---

External API boundaries must enforce the *final wire contract*: only supported parameters, only provider-accepted content shapes, and only schema-valid payloads.

Apply these rules in API-related code (tool dispatchers, transport builders, and request serializers):

1) Filter/allowlist request parameters at every outbound boundary
- Never forward SDK/engine-only kwargs (e.g., overrides consumed by a different provider path).
- Use an explicit allowlist for the JSON/body vs handshake/headers/query.

2) Validate the serialized “on-the-wire” message shape, not the internal shape
- Provider-specific 400s often come from the serialized representation (e.g., an assistant message that is “empty” after serialization).
- Add a final serializer-level sanitizer (after all transforms) that drops/coerces only truly invalid wire shapes.
- If you drop turns, run a role-sequence repair so the history remains valid.

3) Keep JSON schemas consistent with runtime payload contracts
- If payload variants are mutually exclusive (e.g., `mode='replace'` vs `mode='patch'`), the schema must not require both sets of fields.
- Prefer `required: ["mode"]` and enforce per-mode requirements via validator logic or mode-specific constraints in code.

4) Centralize normalization that drives external protocol behavior
- Normalize inputs used for protocol mapping (e.g., file suffixes) once at the boundary (`Path(...).suffix.lower()`), then map to provider-valid formats.
- Propagate the converted artifact path/result back to the caller so the delivery intent matches what was actually generated.

Example (parameter/body allowlist + wire-shape sanitation pattern):
```python
# 1) Boundary allowlist for provider JSON body
WIRE_FIELDS = {"model", "input", "response_format", "temperature", "top_p"}

def build_wire_body(api_kwargs: dict) -> dict:
    body = {k: v for k, v in (api_kwargs or {}).items() if k in WIRE_FIELDS}
    # never include SDK-only controls (extra_headers/extra_body/timeout/stream)
    return body

# 2) Final on-the-wire message sanitizer (after all transforms)

def sanitize_wire_messages(messages: list[dict]) -> list[dict]:
    cleaned = []
    for m in messages:
        if m.get("role") == "assistant" and m.get("content") in (None, "", []) and not m.get("tool_calls"):
            # only drop when it is truly empty on the wire
            continue
        cleaned.append(m)
    # TODO: optionally repair role adjacency if you dropped a turn
    return cleaned
```

Team standard for reviews: if a change touches request building, serialization, tool schemas, or codec/format selection, reviewers should explicitly verify (a) unknown kwargs aren’t forwarded, (b) payloads are schema-valid, and (c) the final serialized wire representation matches what the external service accepts.