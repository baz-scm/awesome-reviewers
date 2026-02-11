---
title: Config schema conventions
description: 'Provide a clear, stable, and discoverable configuration schema. Apply
  the following rules to all TOML/environment configs:


  1) Use self-documenting values'
repository: p-e-w/heretic
label: Configurations
language: Toml
comments_count: 8
repository_stars: 5002
---

Provide a clear, stable, and discoverable configuration schema. Apply the following rules to all TOML/environment configs:

1) Use self-documenting values
- Avoid magic integers/booleans for multi-way choices. Prefer explicit enum/string values. Example: replace direction numeric codes with names:

scorers = [
  { plugin = "heretic.scorers.refusal_rate.RefusalRate", direction = "MINIMIZE", scale = 1.0 }
]

- Use named methods for optional features (future-proofing):

quantization_method = "bnb_4bit"  # instead of load_in_4bit = true

2) Encode mutually exclusive or dependent options as a single enum
- When multiple booleans imply combinations (e.g., compute_normalized & preserve_magnitudes), replace them with an enum so the intent is explicit and invalid combos are impossible:

row_normalization = "none" | "row_normalize" | "row_normalize_and_restore_magnitudes"

3) Standardize plugin-scoped tables and plugin import paths
- Use a documented convention for plugin configuration keys so settings are discoverable and validated. Example conventions:

# For scorer-wide settings
[scorer.RefusalRate]
# For instance-specific settings (suffix with instance name)
[scorer.RefusalRate_instanceA]

- Plugin implementations should be specified as importable module paths (importlib-style). Example:

tagger = "heretic.taggers.keyword.KeywordRefusalDetector"

- If filesystem-path loading is required, document and implement it explicitly; otherwise require importable module paths and document how to extend PYTHONPATH.

4) Validate and warn on conflicts or removed/renamed keys
- Emit a config validation step that:
  - Ensures file ordering/keys are present and documents preferred order (e.g., mirror config.py for readability).
  - Warns when plugin-scoped keys collide with instance-name conventions.
  - Flags removed or interdependent settings (e.g., deprecated kl_divergence_scale/kl_divergence_target) and provide migration guidance.

5) Maintain backward-compatibility with deprecation policy
- When changing a config shape, provide a clear migration path and keep the old key working with warnings for at least one release, or provide a converter tool to update user configs.

How to apply in practice
- Implement a config schema validator that enforces enums, recognized plugin table names (scorer.<ClassName> and scorer.<ClassName>_<instance>), and emits warnings for collisions and deprecated keys.
- Document examples in config.default.toml and note the canonical order (e.g., follow config.py order) so users can scan settings easily.

Example (combined TOML):

# Top-level list of scorers with explicit directions
scorers = [
  { plugin = "heretic.scorers.refusal_rate.RefusalRate", direction = "MINIMIZE", scale = 1.0 }
]

# Plugin path (importable module path)
tagger = "heretic.taggers.keyword.KeywordRefusalDetector"

# Plugin-specific settings
[scorer.RefusalRate]
good_evaluation_prompts = { dataset = "mlabonne/harmless_alpaca", split = "test[:100]", column = "text" }

# Enum-valued options
quantization_method = "bnb_4bit"
row_normalization = "row_normalize_and_restore_magnitudes"

References: discussions 0–7.