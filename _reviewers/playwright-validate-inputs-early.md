---
title: validate inputs early
description: Always validate function parameters and configuration options at the
  beginning of functions, providing specific and actionable error messages that guide
  users toward correct usage. This prevents downstream errors and improves developer
  experience.
repository: microsoft/playwright
label: Error Handling
language: TypeScript
comments_count: 7
repository_stars: 76113
---

Always validate function parameters and configuration options at the beginning of functions, providing specific and actionable error messages that guide users toward correct usage. This prevents downstream errors and improves developer experience.

Key practices:
- Check for required parameters and throw descriptive errors when missing
- Validate parameter types, ranges, and allowed values
- Use specific error messages that indicate what values are expected
- Perform validation before any side effects or expensive operations

Example:
```typescript
static validateNumber(value: string, options: { min?: number, max?: number }): string {
  if (/[^0-9]/.test(value))
    throw new InvalidArgumentError('Not a number.');
  const parsed = parseInt(value, 10);
  if (isNaN(parsed))
    throw new InvalidArgumentError('Not a number.');
  if (options.min !== undefined && parsed < options.min)
    throw new InvalidArgumentError(`Expected a number greater than ${options.min}.`);
  if (options.max !== undefined && parsed > options.max)
    throw new InvalidArgumentError(`Expected a number less than ${options.max}.`);
  return value;
}

// Validate enum values
if (!['begin', 'end'].includes(options.debug))
  throw new Error(`Unsupported debug mode "${options.debug}", must be one of "begin" or "end"`);

// Defensive checks for edge cases
if (!options.expectedText)
  throw new Error('expectedText is required for class validation');
```

This approach catches errors early, provides clear guidance to developers, and prevents cascading failures deeper in the system.