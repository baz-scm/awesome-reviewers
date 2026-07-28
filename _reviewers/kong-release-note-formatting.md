---
title: Release note formatting
description: When updating documentation that is consumed by automated release tooling
  (such as changelog YAML), verify both the semantic classification and the generated
  markdown rendering.
repository: Kong/kong
label: Documentation
language: Yaml
comments_count: 2
repository_stars: 43871
---

When updating documentation that is consumed by automated release tooling (such as changelog YAML), verify both the semantic classification and the generated markdown rendering.

Apply a checklist before merge:
- Set the correct change `type` for the user impact (e.g., if behavior changes and can break workflows, prefer `breaking_change` over `bugfix`).
- Write `message` in a release-friendly structure. If the release generator turns `message` into markdown list items, keep the first line as a short sentence and add clear sub-bullets rather than long, unstructured paragraphs.

Example:
```yml
type: breaking_change
message: |
  Changed the default value of `nginx_http_client_max_body_size` from `0` (unbounded) to `10m`.
  - Requests larger than the new limit may be rejected.
  - Update Kong/Nginx settings if you rely on larger request bodies.
```
