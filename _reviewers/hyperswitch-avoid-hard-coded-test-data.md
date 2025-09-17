---
title: avoid hard-coded test data
description: Hard-coded test data creates maintenance burdens and unrealistic test
  scenarios. Instead of manually defining static values or adding workarounds for
  dynamic fields, leverage existing test utilities and generation functions.
repository: juspay/hyperswitch
label: Testing
language: JavaScript
comments_count: 2
repository_stars: 34028
---

Hard-coded test data creates maintenance burdens and unrealistic test scenarios. Instead of manually defining static values or adding workarounds for dynamic fields, leverage existing test utilities and generation functions.

Use utility functions like `RequestBodyUtils.js` for generating test data dynamically rather than hard-coding values such as customer IDs, amounts, or other parameters. For fields that are inherently dynamic (like authentication data that changes between requests), design tests to either generate appropriate values or properly handle the variability rather than adding comments to "ignore" fields.

Example of improvement:
```javascript
// Instead of:
customer_id: "Customer123_UCS",
amount: 0,

// Use:
customer_id: generateCustomerId(),
amount: generateTestAmount(),
```

This approach reduces test brittleness, improves maintainability, and creates more realistic test scenarios that better reflect production behavior.