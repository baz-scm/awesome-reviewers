---
title: Semantic Naming Rules
description: 'Adopt a naming standard where identifiers encode meaning, don’t clash
  with framework semantics, and don’t obscure behavior.


  Guidelines:

  - Avoid reserved/special filenames and namespace collisions. If a module filename
  has framework semantics (e.g., `api.lua` in plugin contexts), don’t reuse it for
  unrelated code—rename or place code where it can’t be...'
repository: Kong/kong
label: Naming Conventions
language: Other
comments_count: 7
repository_stars: 43871
---

Adopt a naming standard where identifiers encode meaning, don’t clash with framework semantics, and don’t obscure behavior.

Guidelines:
- Avoid reserved/special filenames and namespace collisions. If a module filename has framework semantics (e.g., `api.lua` in plugin contexts), don’t reuse it for unrelated code—rename or place code where it can’t be mistaken.
- Prefer semantic names over comments for basic intent. If a comment explains what a function does, the name likely should include that intent.
  - Example:
    - Bad: `local function set_headers(conf, claims)` with “set header keys from claims” comment.
    - Better: `local function set_headers_from_claims(conf, claims)` (remove the now-redundant comment).
- Make return types match the “has/is” naming contract.
  - Example: `has_capture(...)` should return `true/false` consistently (e.g., `return false`), not `nil`.
- Don’t shadow/repurpose function parameters when their meaning or type changes; this breaks reader expectations.
  - Example: avoid reassigning `value` from `string` to `table` inside the same function.
- Avoid overly-generic identifiers for critical context (e.g., `saved` / `get_saved`). Use names that describe what’s actually being retrieved (request context, saved request headers, etc.), or pass the context explicitly to the handler.
- Use clear boolean helper naming for roles/flags.
  - Example: prefer `is_control_plane(kong.configuration.role)` over raw string comparisons scattered through code.

Impact: improves readability, reduces accidental coupling/namespace bugs, and makes behavior self-evident from names alone.