---
title: Configuration ownership and determinism
description: 'Summary

  - Ensure configuration is explicit, owned by the correct component (application
  vs plugin), and deterministic so behavior is predictable and resumable.'
repository: p-e-w/heretic
label: Configurations
language: Python
comments_count: 25
repository_stars: 5002
---

Summary
- Ensure configuration is explicit, owned by the correct component (application vs plugin), and deterministic so behavior is predictable and resumable.

Why this matters
- Mixing app-level Settings with plugin internal defaults or duplicating metadata produces inconsistencies and surprises for users (e.g. tagger metadata, plugin defaults).
- Silent, environment-specific changes (dtype/device heuristics, implicit reordering of dtypes, magic numbers like LoRA rank) make runs non-reproducible and hard to debug.
- Study resume/checkpointing requires deterministic serialization of the settings that actually affect results.

How to apply (concrete rules)
1) Ownership — plugin-provided defaults and metadata
- Plugins must declare their own config schema and provide defaults/metadata. The application Settings should not duplicate plugin internals.
  - Example pattern (plugin exposes defaults):
    class MyPluginSettings(BaseModel):
        markers: list[str]

    class MyPlugin:
        @classmethod
        def default_settings(cls) -> MyPluginSettings:
            return MyPluginSettings(markers=["I refuse", "sorry"]) 
- At load time the app merges user settings with the plugin defaults returned by the plugin, rather than embedding plugin defaults into global Settings.

2) Deterministic checkpointing and resume
- Serialize the exact Settings that determine study behavior deterministically (sorted keys) and store that serialization alongside any checkpoint/log file. Use that serialized object to compute a resume hash.
  - Example (deterministic JSON hash):
    import json, hashlib
    serialized = json.dumps(settings.model_dump(exclude_none=True), sort_keys=True)
    settings_hash = hashlib.sha256(serialized.encode('utf-8')).hexdigest()
- Save the serialized settings in study metadata (or the checkpoint file) so resume can verify compatibility and users can inspect what was used.
- Make checkpoint directory/name configurable; provide a sensible auto-derived default (e.g. include model name and timestamp) for usability.

3) Explicit, scoped configuration for non-obvious choices
- Surface any "magic numbers" or heuristics as explicit, well-named config fields. Scope names to the feature where they apply to avoid misleading global settings (e.g. full_normalization_lora_rank = 3).
- Document when defaults apply (e.g. "only used when row_normalization == 'full'").

4) Avoid silent platform/environment heuristics
- Do not silently override user-specified config (e.g., reorder dtypes or change dtype cascade) unless the user opts in. If heuristics are necessary, make them opt-in and clearly logged.
- If you must handle platform quirks, document the rule and confine it to a small, explicit code path with a clear config flag.

5) Structured config types and robust parsing
- Use explicit dataclasses/Pydantic models and enums with validators for plugin and app configs. This avoids type/persistence surprises (e.g., enum -> int when restoring) and allows validation.
  - Example: use a Pydantic model with @field_validator to parse legacy values.

6) Precedence and sources
- Define and document settings precedence (CLI vs stored settings vs env vs defaults). When resuming from a stored Settings object, consider treating the stored settings as authoritative for reproducibility; allow intentional overrides but require explicit user action.

7) Prefer maintained utilities over ad-hoc checks
- Reuse tested utilities from dependencies (e.g. reusing rich/_is_jupyter for notebook detection) instead of multiple fragile heuristics.

Checklist for code reviewers
- Does each plugin expose its own settings and defaults? (avoid embedding plugin defaults into global config)
- Are magic numbers surfaced as scoped config fields with clear names and docs?
- Is checkpoint/ resume hashing based on deterministic serialization of the relevant Settings, and is the serialized settings stored with the checkpoint? Is the checkpoint dir/name configurable?
- Are any platform-specific heuristics documented and opt-in? Are silent overrides avoided?
- Are config types structured (dataclass/Pydantic/Enum) and do they include validators to handle persistence or legacy values?

Applying these rules will reduce configuration drift, improve reproducibility (especially for resumable experiments), and make the system easier to understand and extend by ensuring clear ownership and deterministic behavior. 