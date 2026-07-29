---
title: Null and Omission Safety
description: When a config field is optional/nullable (or has multiple shapes), never
  rely on “default” or presence quirks. Make absence vs presence explicit, align schema
  rules with runtime parsing/normalization, and validate the structural inputs that
  runtime can actually interpret.
repository: maximhq/bifrost
label: Null Handling
language: Json
comments_count: 4
repository_stars: 6862
---

When a config field is optional/nullable (or has multiple shapes), never rely on “default” or presence quirks. Make absence vs presence explicit, align schema rules with runtime parsing/normalization, and validate the structural inputs that runtime can actually interpret.

Apply these rules:
- Distinguish “key omitted” from “key present but empty/null”: if a branch should apply only when a field is explicitly empty, encode that with schema logic that won’t accidentally match omitted keys.
- Don’t assume JSON Schema `default` will populate runtime values: implement (and test) normalization during reconciliation/parsing so omitted fields resolve to the correct internal default, while explicit values like `0` are preserved.
- For object-typed variants, require the properties that runtime can’t resolve safely. If runtime parsing only succeeds inside a “value exists” gate, the schema should reject `{}`-like objects so you don’t fall through to unintended plaintext/empty literals.
- Keep “derived” fields out of the source-of-truth validation: if some fields are recomputed from anchors/other totals, enforce ordering/invariants at runtime where the derived value is computed.

Example (absence vs explicit empty mode):
- Avoid a plain `const: ""` if you want to reject cases where `override_mode` is omitted but other override fields are set.
- Instead, use explicit `if/then/else`/`not` logic that makes the empty-mode branch match only when the field is truly in the empty-state, not when it’s missing.

Example (defaults annotation vs runtime normalization):
- Treat schema `default` as documentation.
- Add reconciliation logic like:
  - `if input == nil { resolved = 200 } else { resolved = input }`
  - ensuring `0` stays `0` and omission becomes the intended default.