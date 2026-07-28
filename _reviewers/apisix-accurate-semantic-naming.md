---
title: Accurate Semantic Naming
description: 'Use names that reflect the external meaning and documented behavior—not
  internal implementation details or misleading assumptions.


  **Rules**

  1. **Match the public/schema concept**: For headers, config flags, schema fields,
  provider values, and any user-visible identifiers, use names aligned to the schema
  wording and intent (avoid internal library terms).'
repository: apache/apisix
label: Naming Conventions
language: Other
comments_count: 8
repository_stars: 16922
---

Use names that reflect the external meaning and documented behavior—not internal implementation details or misleading assumptions.

**Rules**
1. **Match the public/schema concept**: For headers, config flags, schema fields, provider values, and any user-visible identifiers, use names aligned to the schema wording and intent (avoid internal library terms).
2. **Name by protocol/operation when behavior is protocol-specific**: If logic is specifically for a protocol operation (e.g., Bedrock “converse”), name the function/entry points accordingly so future protocol additions don’t force renames or confusion.
3. **Ensure the name is behavior-accurate**: Don’t name a function “is_*” unless it truly performs that check. If existing utilities already “resolve if possible,” prefer using those rather than creating a predicate that can’t actually validate the claim.
4. **Keep parameter/flag naming consistent**: Use one agreed term across the codebase (e.g., `commit` vs `dry_run`) and ensure call sites pass the same parameter.
5. **For transformed identifiers, be deterministic and collision-safe**: When generating names (tool names, mapped identifiers, keys), guarantee uniqueness in a stable way and preserve enough mapping to restore the original.

**Example patterns**
- Avoid internal/external mismatch:
  ```lua
  -- Prefer schema-aligned naming
  local raw_id_token = session:get("enc_id_token")
  if raw_id_token and conf.set_raw_id_token_header then
      core.request.set_header(ctx, "X-Raw-ID-Token", raw_id_token)
  end
  ```
- Don’t create misleading predicates; rely on the resolver:
  ```lua
  -- Instead of a fake validator like is_nginx_variable(), use resolve_var
  local resolved, count = core.utils.resolve_var(template)
  if count == 0 then
      -- leave as-is
  end
  ```
- Deterministic collision-safe suffixing for mapped identifiers:
  - Reserve already-valid upstream names and suffix only the rewritten ones, or append a deterministic hash so collisions are impossible by construction while allowing round-trip restoration.