---
title: API Contract Alignment
description: 'Ensure API/event schemas and field names stay consistent across all
  products and generated artifacts.


  Apply this standard when you add/rename fields in request/response payloads, tool/event
  hooks, or persisted protocol types.'
repository: Cline/Cline
label: API
language: Other
comments_count: 2
repository_stars: 70840
---

Ensure API/event schemas and field names stay consistent across all products and generated artifacts.

Apply this standard when you add/rename fields in request/response payloads, tool/event hooks, or persisted protocol types.

- Use a single source of truth for schema/types (e.g., a keys list or schema definition). Regenerate derived files (proto, SDK types, docs) and do not hand-edit generated outputs.
  - Example: after updating the canonical key definition, run the generator and verify the repo has no unintended diffs.

- Align field names across products/consumers.
  - If CLI/Desktop/VS Code currently use different JSON shapes or field names, treat it as a contract bug: track it, fix it, and add compatibility for existing clients.

- When renaming fields, deprecate—not break.
  - Introduce the new canonical name, accept the old one for a defined period, emit warnings/errors only after deprecation, and update docs to clearly label the canonical field.

- Require coverage that proves consistency.
  - Add/extend tests or checks that validate the produced/consumed payload shapes (including renamed/aliased fields) across all relevant entry points (hooks, tools/events, protocol serialization).