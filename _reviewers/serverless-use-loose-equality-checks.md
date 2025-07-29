---
title: use loose equality checks
description: Use loose equality (`== null`) instead of strict equality (`=== null`
  or `=== undefined`) when checking for both null and undefined values. In most JavaScript
  contexts, null and undefined should be treated equivalently, and loose equality
  provides a more concise and readable way to handle both cases.
repository: serverless/serverless
label: Null Handling
language: JavaScript
comments_count: 6
repository_stars: 46810
---

Use loose equality (`== null`) instead of strict equality (`=== null` or `=== undefined`) when checking for both null and undefined values. In most JavaScript contexts, null and undefined should be treated equivalently, and loose equality provides a more concise and readable way to handle both cases.

This pattern is particularly useful for:
- Environment variable checks
- Optional configuration properties  
- Function parameters with default values
- Property existence validation

Example:
```javascript
// Instead of this:
if (typeof process.env[address] === 'undefined') missingEnvVariables.add(address);
if (startingPosition === 'AT_TIMESTAMP' && !(startingPositionTimestamp !== undefined && startingPositionTimestamp !== null)) {

// Use this:
if (process.env[address] == null) missingEnvVariables.add(address);
if (startingPosition === 'AT_TIMESTAMP' && startingPositionTimestamp == null) {
```

The loose equality check (`== null`) catches both `null` and `undefined` values in a single, readable condition, making code more maintainable and following JavaScript's conventional approach to null safety.