---
title: Document Config Semantics
description: 'When adding/changing configuration, make the meaning and lifecycle of
  defaults explicit and consistent.


  Apply this standard:

  - **Unset vs default:** If a value should be optional, represent it as *unset* by
  default and ensure all code paths preserve that (avoid implicit backstop defaults
  that change generated behavior, e.g., DNS records).'
repository: apple/container
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 48787
---

When adding/changing configuration, make the meaning and lifecycle of defaults explicit and consistent.

Apply this standard:
- **Unset vs default:** If a value should be optional, represent it as *unset* by default and ensure all code paths preserve that (avoid implicit backstop defaults that change generated behavior, e.g., DNS records).
- **Optional access consistency:** Use the same “optional-aware” getter semantics across the codebase so you don’t accidentally convert an optional setting into a hardcoded default.
- **Propagation clarity:** In docs, state exactly *when* defaults apply (e.g., only on `create`) and *what* needs to be restarted/stopped (daemon restart vs per-resource stop+restart).
- **Intent-revealing structure:** Organize TOML sections to match operational domains (so config layout communicates which component a setting affects).

Example (DNS optionality + TOML layout):
```toml
# Keep optional until user overrides
[dns]
# domain intentionally omitted (unset)
# domain = "test"  # only set if user wants it
```
```md
# Config docs requirement
- Defaults apply when creating resources: `container machine create ...`
- Existing resources are unchanged
- For `container machine set`, require: stop + restart the machine
```