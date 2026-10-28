---
title: Document only working behavior
description: Documentation must describe the product as it actually behaves, not as
  it was once intended to behave. If a feature, flag, or setting has been removed,
  deprecated, or silently stopped working, delete it from the docs rather than leaving
  a note like "Has no effect" or documenting it as "accepted but ignored" — such hedges
  still imply the option is usable and...
repository: "cline/cline\r\n"
label: Documentation
language: Other
comments_count: 4
repository_stars: 70946
---

Documentation must describe the product as it actually behaves, not as it was once intended to behave. If a feature, flag, or setting has been removed, deprecated, or silently stopped working, delete it from the docs rather than leaving a note like "Has no effect" or documenting it as "accepted but ignored" — such hedges still imply the option is usable and invite readers to rely on it. Only keep a documented caveat for something that is temporarily broken if there's a concrete, near-term plan to fix it; otherwise removal is the right call. For example, prefer deleting a row like `| CLINE_HOOKS_DIR | Has no effect in this release |` entirely instead of keeping it in the reference table.

The same discipline applies to the precision of the language used for working features: choose verbs that match the actual guarantee. Saying a setting is "enforced" when a user can still edit the underlying file between sessions overstates the control: "supports" or "applies" is more accurate. When in doubt, err toward the weaker, more accurate claim and clarify exactly what the product does and does not guarantee, so readers don't build expectations the implementation can't satisfy.