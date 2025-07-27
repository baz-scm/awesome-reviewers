---
title: consistent readable patterns
description: Maintain consistent coding patterns and prioritize readability to make
  code easier to understand and maintain. This includes using consistent approaches
  for similar operations, avoiding overly complex constructions, and ensuring code
  follows predictable patterns.
repository: snyk/cli
label: Code Style
language: TypeScript
comments_count: 12
repository_stars: 5178
---

Maintain consistent coding patterns and prioritize readability to make code easier to understand and maintain. This includes using consistent approaches for similar operations, avoiding overly complex constructions, and ensuring code follows predictable patterns.

Key practices:
- Use consistent patterns for similar operations (e.g., if extracting keys for one object type, do the same for similar objects)
- Avoid mixing different paradigms unnecessarily (e.g., don't mix async/callback syntax)
- Extract complex conditions into well-named boolean functions when they appear multiple times
- Use strict equality (`===`) instead of loose equality (`==`) for predictable comparisons
- Prefer direct, simple approaches over complex constructions when possible

Example of improving consistency:
```typescript
// Inconsistent - different patterns for similar operations
const upgrades = Object.keys(upgrade);
const pins = Object.keys(pin);
if (Object.keys(patch).length) { // Different pattern

// Consistent - same pattern for all similar operations  
const upgrades = Object.keys(upgrade);
const pins = Object.keys(pin);
const patches = Object.keys(patch);
if (patches.length) {
```

Example of extracting complex conditions:
```typescript
// Hard to read when repeated
if (options.iac && options.report && !options.legacy) {

// Extract to descriptive function
const isIacReportFlow = () => options.iac && options.report && !options.legacy;
if (isIacReportFlow()) {
```

This approach reduces cognitive load, makes code more predictable, and helps maintain consistency across the codebase.