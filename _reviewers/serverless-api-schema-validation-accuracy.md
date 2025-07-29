---
title: API schema validation accuracy
description: Ensure that JSON schema validation for API configurations precisely matches
  the actual service requirements and constraints. Schema validation should use correct
  JSON schema properties and accurately reflect documented API limits.
repository: serverless/serverless
label: API
language: JavaScript
comments_count: 7
repository_stars: 46810
---

Ensure that JSON schema validation for API configurations precisely matches the actual service requirements and constraints. Schema validation should use correct JSON schema properties and accurately reflect documented API limits.

Common issues to avoid:
- Using wrong validation properties (e.g., `minLength`/`maxLength` for integers instead of `minimum`/`maximum`)
- Overly restrictive patterns that don't match service capabilities (e.g., JSON pattern allowing only objects when arrays/strings are valid)
- Incorrect constraint values that don't match service documentation (e.g., wrong maximum batch sizes)
- Schema that allows invalid configurations (e.g., array validation that permits partial matches)

Example of correct validation:
```javascript
// Correct: Use proper integer constraints
maximumRetryAttempts: {
  type: 'integer',
  minimum: 0,
  maximum: 185,
}

// Correct: Use enum for exact array matches
AllowedMethods: {
  enum: [['GET', 'HEAD'], ['GET', 'HEAD', 'OPTIONS'], ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH', 'POST', 'DELETE']]
}

// Correct: JSON pattern that matches service capabilities
const jsonPattern = '^\\{.*\\}$'; // Only if service truly requires objects
```

Always verify schema constraints against official service documentation and test edge cases to ensure validation accuracy matches real API behavior.