---
title: Minimize API test data
description: Keep API test configurations lean by including only the fields necessary
  for the specific test scenario. Avoid bloated request/response objects that contain
  extraneous data, and resist creating duplicate API test patterns when existing ones
  can be reused.
repository: juspay/hyperswitch
label: API
language: JavaScript
comments_count: 2
repository_stars: 34028
---

Keep API test configurations lean by including only the fields necessary for the specific test scenario. Avoid bloated request/response objects that contain extraneous data, and resist creating duplicate API test patterns when existing ones can be reused.

This practice improves test maintainability, reduces confusion, and makes test intentions clearer. Before adding new API test configurations, evaluate whether existing patterns can be adapted or if all included fields are truly required for the test case.

Example of bloated vs. minimal API test data:

```javascript
// Bloated - includes unnecessary fields
UCSConfirmMandate: {
  Request: {
    confirm: true,
    customer_id: "Customer123_UCS",
    payment_type: "setup_mandate",
    // ... many other fields that may not be needed for this specific test
    all_keys_required: true,
    metadata: {
      ucs_test: "recurring_payment",
      payment_sequence: "recurring",
    },
  }
}

// Minimal - only necessary fields
UCSConfirmMandate: {
  Request: {
    confirm: true,
    customer_id: "Customer123_UCS",
    payment_type: "setup_mandate",
  }
}
```

When creating new API test commands or configurations, first check if existing patterns can handle your use case to avoid maintenance overhead and confusion.