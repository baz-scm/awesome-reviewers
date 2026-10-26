---
title: Correct Config Semantics
description: When multiple configuration keys exist for related settings (e.g., “deployment
  vs model identity”), verify the runtime meaning of each key and ensure examples/placeholders
  reflect the correct mapping. Also ensure any conditional config logic (feature flags/version
  gating) is accurate, necessary, and easy to read, and that expression comparisons
  use the...
repository: github/docs
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 21111
---

When multiple configuration keys exist for related settings (e.g., “deployment vs model identity”), verify the runtime meaning of each key and ensure examples/placeholders reflect the correct mapping. Also ensure any conditional config logic (feature flags/version gating) is accurate, necessary, and easy to read, and that expression comparisons use the correct types (boolean vs string).

Checklist:
- Identify what each config key controls (routing/deployment vs canonical model identity) and avoid swapped assignments.
- Keep placeholders aligned with the corrected semantics, and cross-check any fallback/resolution keys (e.g., a CLI’s primary model identifier).
- Prefer simplifying templated conditions when the output is guaranteed (remove unnecessary branching).
- In expression/config logic, compare booleans to booleans (not `'true'`), and ensure you only use supported contexts/variables.

Example (environment variables):
```shell
# Correct mapping: deployment name routes the request; model identity drives model capabilities.
export COPILOT_PROVIDER_BASE_URL=https://YOUR-RESOURCE-NAME.openai.azure.com
export COPILOT_PROVIDER_TYPE=azure
export COPILOT_PROVIDER_API_KEY=YOUR-AZURE-API-KEY
export COPILOT_PROVIDER_AZURE_API_VERSION=YOUR-AZURE-API-VERSION
export COPILOT_PROVIDER_MODEL_ID=YOUR-MODEL-NAME
export COPILOT_PROVIDER_WIRE_MODEL=YOUR-DEPLOYMENT-NAME
# Optionally confirm whether COPILOT_MODEL should match which identifier the CLI resolves against.
```