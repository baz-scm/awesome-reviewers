---
title: Semantic naming conventions
description: 'Use descriptive, semantic names for all code elements that clearly indicate
  their purpose and behavior. Follow consistent casing patterns throughout the codebase:'
repository: aws/aws-sdk-js
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 7628
---

Use descriptive, semantic names for all code elements that clearly indicate their purpose and behavior. Follow consistent casing patterns throughout the codebase:

- camelCase for variables, properties, and method names (e.g., 'useDualstack', 'bucketExists')
- PascalCase for class names and type definitions
- When naming functions, prefer names that describe what the function does rather than implementation details (e.g., 'buildMessage' is clearer than 'formatMessage')
- Avoid abbreviations that aren't widely understood (e.g., use 'optionalDiscoveryEndpoint' instead of 'optionalDisverEndpoint')
- When type names conflict with JavaScript primitives, use a prefix (e.g., '_Date') rather than skipping the type definition entirely to prevent runtime errors

```javascript
// Poor naming
function getServiceClock() {
  return new Date(Date.now() + this.config.systemClockOffset);
}

// Better naming
function getSkewCorrectedDate() {
  return new Date(Date.now() + this.config.systemClockOffset);
}

// Poor type handling - skipping shapes that match JavaScript primitives
if (['string', 'boolean', 'number', 'Date', 'Blob'].indexOf(shapeKey) >= 0) {
  return '';
}

// Better type handling - using prefix to preserve shape names
if (['string', 'boolean', 'number', 'Date', 'Blob'].indexOf(shapeKey) >= 0) {
  code += 'export type _' + shapeKey + ' = ' + getTypeMapping(shape.type) + ';\n';
  return code;
}
```
