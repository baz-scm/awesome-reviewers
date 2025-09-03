---
title: Use descriptive testing names
description: Ensure all testing-related identifiers, scripts, and messages use clear,
  descriptive names rather than abbreviations or overly specific terminology. This
  improves maintainability and reduces confusion for both developers and users.
repository: cypress-io/cypress
label: Testing
language: Json
comments_count: 2
repository_stars: 48850
---

Ensure all testing-related identifiers, scripts, and messages use clear, descriptive names rather than abbreviations or overly specific terminology. This improves maintainability and reduces confusion for both developers and users.

For script names, prefer explicit over abbreviated versions:
```json
// Good
"cypress:open": "ts-node ../../scripts/start.js --component-testing --project ${PWD}",
"cypress:run": "ts-node ../../scripts/start.js --component-testing --run-project ${PWD}",

// Avoid
"cy:open": "ts-node ../../scripts/start.js --component-testing --project ${PWD}",
"cy:run": "ts-node ../../scripts/start.js --component-testing --run-project ${PWD}",
```

For user-facing messages, use parameterized or generic terminology when possible to support multiple testing contexts:
```json
// Good - flexible for different testing types
"text": "You can reconfigure the {testingType} testing settings for this project if you're experiencing issues with your Cypress configuration."

// Avoid - too specific
"text": "You can reconfigure the component testing settings for this project if you're experiencing issues with your Cypress configuration."
```

This approach makes testing tooling more discoverable and user-facing content more reusable across different testing scenarios.