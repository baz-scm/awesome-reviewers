---
title: Semantic version bumps
description: When a change alters default parameter values, default behavior, or import/module
  structure, treat it as a breaking change for semantic-versioning purposes even if
  no function signature is removed. Bump the minor version (x.Y.0) rather than only
  the patch version (x.y.Z) in these cases, since downstream consumers often pin or
  branch on version ranges (e.g.,...
repository: run-llama/llama_index
label: Migrations
language: Toml
comments_count: 4
repository_stars: 52785
---

When a change alters default parameter values, default behavior, or import/module structure, treat it as a breaking change for semantic-versioning purposes even if no function signature is removed. Bump the minor version (x.Y.0) rather than only the patch version (x.y.Z) in these cases, since downstream consumers often pin or branch on version ranges (e.g., `< 0.6`) and a silent patch bump can break their code when defaults change under them. Before merging a release PR, check pyproject.toml version bumps against the actual nature of the change: pure bug fixes and non-behavioral tweaks can stay as patch bumps, but any change to defaults (e.g., a boolean flag switching from `False` to `True`), altered import paths, or other behavior-affecting changes should prompt a minor bump instead.

Example:
```toml
# Before: use_file_api defaulted to False
# After: use_file_api defaults to True
[project]
name = "llama-index-llms-google-genai"
-version = "0.3.2"
+version = "0.4.0"  # minor bump because default behavior changed
```