---
title: Strict auth schema validation
description: 'Security-related Helm/config schemas should fail fast on invalid or
  unintended authentication settings.


  Apply:

  - Close security-sensitive objects with `additionalProperties: false` so typos/mistyped
  fields are rejected at `helm template`/validation time (instead of silently producing
  insecure runtime behavior).'
repository: maximhq/bifrost
label: Security
language: Json
comments_count: 2
repository_stars: 6862
---

Security-related Helm/config schemas should fail fast on invalid or unintended authentication settings.

Apply:
- Close security-sensitive objects with `additionalProperties: false` so typos/mistyped fields are rejected at `helm template`/validation time (instead of silently producing insecure runtime behavior).
- When auth is enabled, model credentials as required structured fields (e.g., require `credentials.name` and `credentials.key` when auth is on).
- Reuse shared, closed definitions for repeated security sub-structures (e.g., relabeling blocks) so misspellings like `sourceLables` don’t slip through.
- Ensure provider-scoped security flags are only accepted for intended providers: don’t let permissive parent schema parts (e.g., `base_key`) implicitly allow unrelated security flags.

Example pattern (ServiceMonitor-style strict auth):
```json
{
  "authorization": {
    "type": "object",
    "description": "Bearer-token auth for scrape",
    "additionalProperties": false,
    "properties": {
      "type": {"type": "string"},
      "credentials": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "name": {"type": "string"},
          "key": {"type": "string"}
        },
        "required": ["name", "key"]
      }
    },
    "required": ["type", "credentials"]
  }
}
```

Outcome: invalid auth configs (typos, missing required credential fields, or flags applied to the wrong provider) are rejected early, preventing insecure or broken authentication behavior at runtime.