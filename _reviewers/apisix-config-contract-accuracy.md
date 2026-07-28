---
title: Config Contract Accuracy
description: 'Ensure configuration documentation and validation rules match the real
  runtime contract: types/structures, default values, actual scope, and when validation
  happens.'
repository: apache/apisix
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 16922
---

Ensure configuration documentation and validation rules match the real runtime contract: types/structures, default values, actual scope, and when validation happens.

Apply these checks to every configurable field:
1) **Type/shape must support the operational use-case**
- If the setting naturally represents multi-dimensional filtering or staged rollouts, document/implement it as a multi-value structure (e.g., arrays) rather than forcing single-string workarounds.
```json
// Prefer multi-value matching to support canary/prod-blue/prod-green without extra keys
"discovery_args": {
  "metadata_match": {
    "env": ["canary", "prod-blue", "prod-green"],
    "version": ["v1", "v2"]
  }
}
```

2) **Be explicit about validation bypass vs runtime resolution**
- If config loading bypasses schema constraints due to secret/env reference resolution, state it clearly and rely on runtime validation after resolution.
```text
Use $secret://... or $env://... in plugin string fields.
Schema constraints apply to the resolved value at runtime, not during config loading.
```

3) **Document true blast radius (shared/core toggles)**
- If a configuration value is implemented via a shared core helper used by multiple plugins/features, document that it impacts all of them—do not scope it to the feature name in the doc.

4) **Align documented defaults with code**
- Verify every documented default equals the implementation default (including nested/batch helper defaults). If other components already fixed mismatches, update the remaining ones the same way.

This prevents configuration drift, misleading docs, and rollout-time surprises—especially for environment-specific settings and feature flags.