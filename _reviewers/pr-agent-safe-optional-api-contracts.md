---
title: Safe, Optional API Contracts
description: 'When designing API responses and client-triggered actions, keep contracts
  accurate and defaults safe:


  1) Make optional data optional in response schemas'
repository: the-pr-agent/pr-agent
label: API
language: Toml
comments_count: 2
repository_stars: 12523
---

When designing API responses and client-triggered actions, keep contracts accurate and defaults safe:

1) Make optional data optional in response schemas
- If a field is not guaranteed to exist for every request/PR, do not force it in the schema.
- Concretely: ensure the schema does not list the field under required properties, so “Score” can be omitted.

Example (JSON Schema pattern):
```json
{
  "type": "object",
  "properties": {
    "Score": { "type": "number" }
  }
  /* Intentionally omit "required": ["Score"] */
}
```

2) Choose non-destructive defaults for actions clients trigger
- For event-driven “commands” or default behaviors exposed via an API/integration, avoid actions described as destructive or irreversible.
- If an action must remain default, constrain it with least-destructive flags so it preserves user content; otherwise remove it from defaults.

Example (least-destructive default behavior):
```bash
/describe --pr_description.add_original_user_description=true \
          --pr_description.keep_original_user_title=true
# If still considered too risky, remove /describe from default command list and keep only:
/auto_review
```

Apply this standard whenever you change: API response formats, webhook-driven bot behaviors, default command/action lists, or schema definitions used by clients.