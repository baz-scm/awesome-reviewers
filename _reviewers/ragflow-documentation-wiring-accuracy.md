---
title: Documentation Wiring Accuracy
description: 'Ensure technical documentation is both semantically correct and operationally
  precise: (1) use the exact product terms for what a setting applies to (scope/terminology),
  and (2) when describing component internals/graphs, specify the exact wiring rule
  for references (use the internal managing node, not an external component), aligned
  with the documented...'
repository: infiniflow/ragflow
label: Documentation
language: Other
comments_count: 2
repository_stars: 80174
---

Ensure technical documentation is both semantically correct and operationally precise: (1) use the exact product terms for what a setting applies to (scope/terminology), and (2) when describing component internals/graphs, specify the exact wiring rule for references (use the internal managing node, not an external component), aligned with the documented visibility constraints.

How to apply:
- Scope/terminology check: If a doc claims that a config limit “applies to X,” confirm the exact system feature name and what scenario it does/does not apply to.
- Graph/reference check: For internal workflows, document the concrete reference variable to use (e.g., the internal loop controller/seed node) and explicitly state when external references are unnecessary.

Example (Iteration internal wiring pattern):
```mdx
:::danger IMPORTANT
To reference the created segments from an added internal component, add a **Reference** variable that equals **IterationItem** within the **Input** section of that internal component. There is no need to reference the corresponding external component, as the **IterationItem** component manages the loop of the workflow for all created segments.
:::
```

Example (setting scope/terminology):
```mdx
The variables `MAX_CONTENT_LENGTH` in `/docker/.env` and `client_max_body_size` in `/docker/nginx/nginx.conf` set the file size limit for each upload to a dataset or **File**. These settings DO NOT apply in this scenario.
```