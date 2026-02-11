---
title: Use clear names
description: 'Rule: choose concise, semantically accurate, and responsibility-respecting
  names for identifiers (variables, functions, classes, modules). Motivation: clear
  names reduce cognitive load, avoid ambiguity, and prevent leaking responsibilities
  across layers.'
repository: p-e-w/heretic
label: Naming Conventions
language: Python
comments_count: 11
repository_stars: 5002
---

Rule: choose concise, semantically accurate, and responsibility-respecting names for identifiers (variables, functions, classes, modules). Motivation: clear names reduce cognitive load, avoid ambiguity, and prevent leaking responsibilities across layers.

Guidelines:
- Prefer concise domain nouns; drop redundant suffixes or qualifiers. Example: use tagger (not tagger_plugin), directory name taggers (not taggers_plugin). For classes, avoid duplicative internal fields like _categorical when the class name already communicates the type.
  - Bad: tagger_plugin: str
  - Good: tagger: str

- Make names reflect their return type/semantics. Use verbs for actions and nouns for data; name boolean flags clearly. Examples:
  - get_trials_completed() -> count_completed_trials()  # returns int
  - get_* should return objects or collections; count_/is_/has_ for predicates or numeric counts.

- For binary options prefer a boolean with a neutral name rather than a Literal with two labels. Example:
  - mode: Literal["remove_inhibitions","increase_inhibitions"] -> reverse: bool = False

- Express units and domains in names. If a value is a fraction (0..1), name it accordingly. Example:
  - winsorization_level (0..100) -> winsorization_quantile (0.0..1.0)

- Do not embed UI/label or management concerns inside low-level classes. E.g., avoid passing instance_name or display labels into classes that represent logic; labeling/aggregation belongs to higher-level code.
  - Bad: Scorer(..., instance_name=...)
  - Good: keep Scorer focused on behavior; management code assigns names/labels.

- Flatten and standardize config types for plugins. Prefer a nested Settings model named Settings or a top-level Settings type over nonstandard nested names like PluginSettings. This keeps plugin initialization consistent.
  - Bad: class KLDivergence(Scorer): class PluginSettings(BaseModel): ...
  - Good: class KLDivergence(Scorer): class Settings(BaseModel): ... or unnest to module-level Settings.

- Keep internal naming consistent; map to user-facing labels only at presentation boundaries. If internal code uses scores, stick with scores; render them as "Metrics" only in displays.

Code examples:
- Rename and semantics:
  - Before: study_name = "heretic_study_" + "_".join(study_components)
  - After: study_name = "_".join(study_components)  # omit unnecessary prefix

- Function naming:
  - Before: def get_trials_completed() -> int: ...
  - After: def count_completed_trials() -> int: ...

Application checklist for reviewers:
1. Ask: Is any word redundant given the type or context? Remove it. (e.g., _plugin, _categorical)
2. Ask: Does the name indicate the value’s type/unit/semantics? If not, clarify (e.g., _quantile, is_*, count_*).
3. Ask: Is responsibility leaking into this identifier? Move UI/label/instance concerns out of logical classes.
4. Verify consistency across modules (e.g., scores vs metrics) and pick a single internal term.

References: discussion indices [0,1,3,4,6,7,8,10,11,12,13].