---
title: Meaningful documentation practices
description: Documentation should enhance code understanding rather than duplicate
  information already present in the code. Avoid redundant type annotations in JSDoc
  when type systems like Flow are already used. Instead, focus on explaining intent,
  complex logic, and providing context that aids debugging and maintenance.
repository: facebook/react-native
label: Documentation
language: JavaScript
comments_count: 3
repository_stars: 123178
---

Documentation should enhance code understanding rather than duplicate information already present in the code. Avoid redundant type annotations in JSDoc when type systems like Flow are already used. Instead, focus on explaining intent, complex logic, and providing context that aids debugging and maintenance.

For test descriptions, use clear, descriptive names that explain the feature being tested:
```javascript
// Good: Explains the feature being tested
describe('Testing Cancel Button Functionality', function () {

// Avoid: Vague or redundant descriptions  
describe('Test is checking cancel button', function () {
```

For complex patterns like regular expressions, add explanatory comments:
```javascript
// Good: Explains what the regex matches
const colorStopRegex = 
  // matches color values like rgba(0,0,0,1), #fff, or named colors with optional percentages
  /\s*((?:(?:rgba?|hsla?)\s*\([^)]+\))|#[0-9a-fA-F]+|[a-zA-Z]+)(?:\s+(-?[0-9.]+%?)(?:\s+(-?[0-9.]+%?))?)?\s*/gi;
```

Prioritize documentation that tells developers why something exists or how it works, not what is already evident from well-written code.