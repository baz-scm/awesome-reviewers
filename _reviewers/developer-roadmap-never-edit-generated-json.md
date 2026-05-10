---
title: Never edit generated JSON
description: Treat any build/CI-generated JSON (and files under similar “public/…-content”
  paths) as read-only. Don’t patch them directly in PRs—changes will be overwritten
  or won’t propagate.
repository: kamranahmedse/developer-roadmap
label: CI/CD
language: Json
comments_count: 3
repository_stars: 354523
---

Treat any build/CI-generated JSON (and files under similar “public/…-content” paths) as read-only. Don’t patch them directly in PRs—changes will be overwritten or won’t propagate.

How to apply:
- Find the upstream source used by the generator (e.g., templates, content definitions, or the build script/config).
- Make the change there.
- Regenerate the JSON via the normal pipeline/build step and verify the output.

Example (PR rule of thumb):
- ❌ Commit to: `public/roadmap-content/*.json` (auto-generated output)
- ✅ Commit to: the generator input/template/source, then run the build to update the generated JSON automatically.