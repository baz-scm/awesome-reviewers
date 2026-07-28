---
title: API contract consistency
description: 'When defining or documenting APIs/plugins, ensure the declared contract
  matches how the system actually resolves requests and config fields. Validate examples
  and client expectations against these checks:'
repository: apache/apisix
label: API
language: Markdown
comments_count: 5
repository_stars: 16922
---

When defining or documenting APIs/plugins, ensure the declared contract matches how the system actually resolves requests and config fields. Validate examples and client expectations against these checks:

1) Route matching must cover the real request path
- If users will request `/prefix/suffix`, don’t configure only `/prefix`; use `/prefix/*` (or the equivalent wildcard/prefix controller syntax).

2) Request body/encoding must match extraction rules
- If a config uses `$post_arg.<field>`, the request must send form-style POST args (typically `application/x-www-form-urlencoded`).
- If the client sends JSON, you must either switch the approach to JSON extraction (where supported) or change the example to form encoding.

Example (consistent with `$post_arg.tenant_id`):
```sh
curl -i "http://127.0.0.1:9080/post" -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'tenant_id=000'
```

3) Keep API config field types aligned with upstream/integration contracts
- Prefer the simplest type that matches what upstream systems naturally provide (e.g., `string:string` metadata).
- If you must support multiple shapes later, introduce a documented union (e.g., `string|string[]`) rather than silently mixing incompatible formats.

4) Use the correct framework primitives/wiring
- For request mutation, prefer the dedicated setter APIs (e.g., setting URI args via `core.request.set_uri_args`) rather than relying on side effects.
- For interface integrations (e.g., Gateway API), use the correct extension/wiring pattern for that API surface.

Adopt this as a “pre-merge” checklist item for any API-facing documentation or examples: run through the exact request path and encoding, confirm the resolved variables/fields, and ensure the config schema types reflect the real integration contract.