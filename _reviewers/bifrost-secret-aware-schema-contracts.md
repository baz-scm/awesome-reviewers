---
title: Secret-Aware Schema Contracts
description: 'When updating configuration schemas (and related env/test fixtures),
  treat the schema as a contract with runtime unmarshalling and deployment timing.

  '
repository: maximhq/bifrost
label: Configurations
language: Json
comments_count: 4
repository_stars: 6862
---

When updating configuration schemas (and related env/test fixtures), treat the schema as a contract with runtime unmarshalling and deployment timing.

Apply these rules:
1) Mirror secret-aware runtime types in the schema
- If the runtime config uses secret variables that accept either a plain string or a structured secret object, model credential fields the same way (don’t restrict to string only).

Example pattern (JSON Schema):
```json
{
  "anyOf": [
    { "type": "string" },
    {
      "type": "object",
      "properties": {
        "value": { "type": "string" },
        "env_var": { "type": "string" },
        "from_env": { "type": "boolean" }
      },
      "required": ["value"],
      "additionalProperties": false
    }
  ]
}
```

2) Verify the config effect end-to-end (release coupling)
- If the schema change introduces a new field consumed only by a different repo/service, ensure the corresponding runtime wiring will ship in the same release; otherwise the field may validate but behave like a no-op.

3) Avoid out-of-scope “partial tightening”
- Don’t change schema enums to match runtime allowlists unless the change is intentional and scoped; if runtime already enforces support via a separate validator, understand that schema passes may be an accepted pre-existing behavior.

4) Keep test/env files suite-scoped
- Only define keys that the specific test suite consumes. Don’t add placeholder vars from other suites to “silence” missing placeholders—this creates divergence and false confidence.

Outcome: schema validation should align with real runtime parsing, and “valid configs” should produce the intended behavior in the correct release.