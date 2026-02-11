---
title: consistent identifier naming
description: "Prefer clear, consistent, and semantic names for variables, classes,\
  \ config keys, and section labels. Use these concrete rules when naming: \n\n- Use\
  \ nouns for metrics/objects and verbs for actions. Prefer semantically meaningful\
  \ units (e.g., use RefusalRate rather than CountRefusals) so scales are interpretable\
  \ and independent of context:"
repository: p-e-w/heretic
label: Naming Conventions
language: Toml
comments_count: 3
repository_stars: 5002
---

Prefer clear, consistent, and semantic names for variables, classes, config keys, and section labels. Use these concrete rules when naming: 

- Use nouns for metrics/objects and verbs for actions. Prefer semantically meaningful units (e.g., use RefusalRate rather than CountRefusals) so scales are interpretable and independent of context:
  # bad
  scorers = [ ["heretic.scorers.count_refusals.CountRefusals", "minimize", 1.0] ]
  # good
  scorers = [ ["heretic.scorers.refusal_rate.RefusalRate", "minimize", 1.0] ]

- Make units explicit in the name when scale matters (Rate, Count, Score, Probability). If a value depends on dataset size, prefer a rate or normalized form.

- Namespace plugin/config sections by type to improve discoverability and avoid name collisions. Prefer hierarchical section names for plugin classes: e.g. use scorer.RefusalRate instead of a top-level [RefusalRate] when the setting belongs to scorers:
  # good
  [scorer.RefusalRate]
  threshold = 0.05

- Keep boolean/flag names concise and consistent in voice and plurality. Avoid long ad-hoc prefixes unless they add meaning; use a stable verb form (orthogonalize_*, preserve_*) and consistent plurality:
  # bad
  abliteration_orthogonal_project = false
  abliteration_preserve_magnitude = false
  # better
  orthogonalize_direction = false
  preserve_magnitudes = false

- Balance namespacing with CLI ergonomics. If deep nesting would complicate common overrides, prefer a flat name that remains concise and consistent; otherwise prefer namespacing for clarity.

Checklist to apply during review:
- Is the identifier a noun (object/metric) or verb (action)? Does the form match its role?
- Does the name include units/scale when needed (Rate/Count/etc.)?
- Are section/table names grouped by category (scorer/, modifier/, etc.)?
- Are boolean flags concise and consistent in verb/noun order and plurality?
- Would namespacing harm common operations (CLI overrides)? If so, choose a shorter flat name following the same conventions.

Following these rules reduces ambiguity, makes configuration values interpretable (especially scales), and keeps naming consistent across code and config.