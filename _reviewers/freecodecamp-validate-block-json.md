---
title: Validate Block JSON
description: 'Ensure every `curriculum/structure/blocks/*.json` file matches the CI-validated
  schema and constraints.


  - Remove deprecated/unused fields (e.g., `name`)—CI may reject these.'
repository: freeCodeCamp/freeCodeCamp
label: CI/CD
language: Json
comments_count: 10
repository_stars: 444449
---

Ensure every `curriculum/structure/blocks/*.json` file matches the CI-validated schema and constraints.

- Remove deprecated/unused fields (e.g., `name`)—CI may reject these.
- Ensure required identifiers conform to CI rules (e.g., block/challenge `id` must be valid and not too short).
- If CI fails, fix the JSON payload in the same branch (don’t rely on retries).

Example (schema-compliant style):
```json
{
  "isUpcomingChange": false,
  "dashedName": "workshop-envelope-budget-app",
  "helpCategory": "HTML-CSS",
  "blockLayout": "challenge-grid",
  "blockLabel": "workshop",
  "challengeOrder": [
    { "id": "<valid-id-length-and-format>", "title": "Step 1" }
  ]
}
```