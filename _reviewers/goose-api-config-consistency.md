---
title: API Config Consistency
description: Declarative API/provider configurations must be internally consistent
  with (a) the canonical identifiers used by the model registry/discovery layer and
  (b) the request-building logic that actually emits fields for the selected engine/path.
  This prevents mismatches, silent capability drops, and confusing “it’s configured
  but doesn’t work” behavior.
repository: aaif-goose/goose
label: API
language: Json
comments_count: 2
repository_stars: 51876
---

Declarative API/provider configurations must be internally consistent with (a) the canonical identifiers used by the model registry/discovery layer and (b) the request-building logic that actually emits fields for the selected engine/path. This prevents mismatches, silent capability drops, and confusing “it’s configured but doesn’t work” behavior.

Apply these checks when adding/updating provider JSON:
1) Canonicalize model IDs
- If live endpoints return variant names/suffixes, ensure the static model entries use the canonical registry IDs expected by discovery/filters (so static fallback and dynamic discovery resolve to the same model).

2) Make capability flags truthful
- Only set capability flags (e.g., reasoning/thinking) if the generic request builder for that engine/path will emit the corresponding request fields.
- If the path would silently drop the value (no emitted top-level field / different schema), remove the capability flag rather than advertise unsupported behavior.

Example pattern (canonical ID + truthful capability):
```json
{
  "name": "example-provider",
  "engine": "openai",
  "api_key_env": "EXAMPLE_TOKEN",
  "models": [
    {
      "name": "vendor/Canonical-Model-ID", 
      "context_limit": 123456,
      "reasoning": true
      /* reasoning is only true if the request builder emits the needed field for this model path */
    }
  ]
}
```
If you’re unsure whether a capability is emitted for a given model/engine path, prefer “capability off” over a misleading on-flag, or implement the necessary request-layer support (with a clear, testable mapping).