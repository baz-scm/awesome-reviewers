---
title: Semantic identifier naming
description: Use semantic, unambiguous names for every externally visible identifier
  (API parameters/endpoints, config/env vars, and build/version tags). Names must
  reflect meaning and supported behavior; if an operation is not supported, document
  that constraint next to the relevant field/behavior.
repository: infiniflow/ragflow
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 80174
---

Use semantic, unambiguous names for every externally visible identifier (API parameters/endpoints, config/env vars, and build/version tags). Names must reflect meaning and supported behavior; if an operation is not supported, document that constraint next to the relevant field/behavior.

Application rules:
- API naming: prefer consistent, descriptive snake_case names for parameters (e.g., `parent_id`, `file_ids`, `page_size`, `orderby`, `desc`) and keep them aligned with the actual request/response contract.
- API constraints: when behavior is restricted, state it explicitly (e.g., “Changing file extensions is *not* supported.”) so users don’t infer unsupported semantics from the parameter/field naming.
- Build/release naming: standardize version tag labels so stability and feature set are obvious.
  - Use `vX.Y.Z` for stable releases.
  - Use `vX.Y.Z-slim` for stable “slim” variants.
  - Use `dev` (not ambiguous labels like `dev1`) for development images.
  - Use `nightly` for nightly builds.

Example (Docker tag standard):
```text
RAGFLOW_IMAGE=infiniflow/ragflow:v0.14.1
RAGFLOW_IMAGE=infiniflow/ragflow:v0.14.1-slim
RAGFLOW_IMAGE=infiniflow/ragflow:dev
RAGFLOW_IMAGE=infiniflow/ragflow:nightly
```

Example (API constraint wording):
```text
POST /api/v1/file/rename
Body: { "file_id": "...", "name": "new_name.txt" }
Note: Changing file extensions is not supported.
```