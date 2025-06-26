---
title: "Extract for better readability"
description: "Complex expressions and repeated code should be extracted into well-named variables to improve readability and maintainability. This applies to repeated string/value combinations, complex conditional logic, array transformations, and URL or path constructions."
repository: "axios/axios"
label: "Code Style"
language: "JavaScript"
comments_count: 4
repository_stars: 107000
---

Complex expressions and repeated code should be extracted into well-named variables to improve readability and maintainability. This applies to:
- Repeated string/value combinations
- Complex conditional logic
- Array transformations
- URL or path constructions

Example - Instead of:
```javascript
if ([options.path, responseDetails.headers.location].every(item => item === '/foo')) {
  // ...
}
```

Better approach:
```javascript
const isPathMatching = options.path === '/foo';
const isLocationMatching = responseDetails.headers.location === '/foo';
if (isPathMatching && isLocationMatching) {
  // ...
}
```

This practice:
- Makes code self-documenting through meaningful variable names
- Reduces cognitive load when reading complex logic
- Makes debugging easier by providing clear intermediate values
- Prevents duplicate calculations