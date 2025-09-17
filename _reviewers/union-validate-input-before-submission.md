---
title: Validate input before submission
description: Always validate user input before enabling form submission to prevent
  processing of invalid or malicious data. This includes checking for empty required
  fields, format validation, and business logic constraints. Implement validation
  checks in the form's disabled state or submission handler to ensure only valid data
  can be processed.
repository: unionlabs/union
label: Security
language: Other
comments_count: 1
repository_stars: 74800
---

Always validate user input before enabling form submission to prevent processing of invalid or malicious data. This includes checking for empty required fields, format validation, and business logic constraints. Implement validation checks in the form's disabled state or submission handler to ensure only valid data can be processed.

Example implementation:
```javascript
// Disable submit button when validation fails
disabled={$faucetState.kind !== "IDLE" || isValidCosmosAddress(address, ['union']) === false}
```

This pattern prevents users from submitting forms with empty addresses, invalid formats, or when the application is in an inappropriate state. Client-side validation improves user experience while server-side validation provides security protection against malicious requests.