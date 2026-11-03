---
title: Semantic and consistent identifier naming
description: Names for variables, parameters, methods, and fields must be accurate,
  unambiguous, and consistent with existing conventions elsewhere in the codebase.
repository: run-llama/llama_index
label: Naming Conventions
language: Python
comments_count: 9
repository_stars: 52785
---

Names for variables, parameters, methods, and fields must be accurate, unambiguous, and consistent with existing conventions elsewhere in the codebase.

- Choose names that reflect the actual content/type, not a misleading approximation. For example, a parameter accepting a single string should be named `prompt`, not `texts`; a field holding arbitrary user-supplied data should be `custom_fields`, not the vague `extra_fields`; a variable should not be named `image_nodes` if it's untyped/`Any` and doesn't clearly hold image nodes.
- Callback parameters should make their nature obvious from the name, e.g. `file_exists_callback` rather than `check_file_exist`.
- Follow established prefixing conventions for async variants: use the same `a`-prefix pattern consistently with sibling methods (e.g. if `aput` exists, the matching getter should be `aget`, not `get`). When the base method name starts with a vowel, use `async_` instead of a bare `a` prefix (e.g. `_async_ensure_initialized`, not `_aensure_initialized`) to preserve readability.
- Respect the public/private naming convention: do not export names prefixed with `_` through a package's public `__init__.py`; either make them public (drop the underscore) or keep them internal.
- When adding new metadata keys, delimiters, or method names, check for and follow conventions already established by sibling readers/integrations/agents (e.g. reuse `page_label` instead of introducing a redundant `slide_number` key; reuse `start`/`stop` method names used by other voice agent implementations rather than introducing `run`). Also verify that any new delimiter or separator character cannot collide with legal characters in the data it's splitting (e.g. avoid `_` as a separator for IDs that may themselves contain `_`).
- Avoid breaking renames to existing public parameters/fields unless necessary; if a rename is required, bump the package version accordingly.