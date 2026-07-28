---
title: Validate Inputs Securely
description: Treat runtime-derived values (env vars, request data, rendered attributes)
  as untrusted unless they’re validated by the framework’s schema/typedefs or hardened
  with allowlists.
repository: Kong/kong
label: Security
language: Other
comments_count: 5
repository_stars: 43871
---

Treat runtime-derived values (env vars, request data, rendered attributes) as untrusted unless they’re validated by the framework’s schema/typedefs or hardened with allowlists.

Checklist:
- Prefer typedefs/schema validation over raw `string`/ad-hoc parsing for security-sensitive fields (URLs, crypto material, etc.).
- For crypto keys, use `typedefs.key` (and restrict/validate key type/algorithm, e.g., RSA vs EC).
- Don’t let environment variables directly control production-sensitive paths/behavior; gate with explicit allowlisted logic (dev vs prod) or generate the needed config at build time.

Examples:
- Redirect URL validation:
```lua
location = typedefs.url
```
- Public key schema:
```lua
type = "record",
-- ...
public_key = typedefs.key {
  description = "The RSA public key used to validate signature.",
  encrypted = true,
  referenceable = true,
}
```
- Avoid unsafe env-driven paths by gating:
```lua
local prefix = "/usr/local/kong"
if kong_config.development then
  prefix = os.getenv("KONG_LIBRARY_PREFIX") or prefix -- allowlisted dev override only
end
prepare_prefixed_interface_dir(prefix, "gui", kong_config)
```

Apply this consistently to prevent path traversal/config injection, incorrect header handling, and weak or missing validation for URLs and cryptographic inputs.