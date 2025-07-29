---
title: Structure configs for clarity
description: 'Organize configuration objects to maximize clarity and maintainability
  while ensuring robust validation. Follow these principles:


  1. Use single object definitions instead of multiple configurations to enable specific
  error messages'
repository: serverless/serverless
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 46810
---

Organize configuration objects to maximize clarity and maintainability while ensuring robust validation. Follow these principles:

1. Use single object definitions instead of multiple configurations to enable specific error messages
2. Include sensible defaults and clear fallback behavior
3. Validate at schema level when possible, but move complex validations to code level
4. Ensure error messages clearly indicate the misconfigured property

Example of good configuration structure:

```javascript
// Instead of multiple object configurations:
{
  oneOf: [
    { type: 'string' },
    { type: 'object',
      properties: { ... } 
    }
  ]
}

// Use single object with clear validation:
{
  type: 'object',
  properties: {
    type: { type: 'string' },
    arn: { type: 'string' }
  }
}

// Then validate complex rules in code:
if (config.arn && !isValidArn(config.arn)) {
  throw new Error('Invalid ARN format provided');
}
```

This approach ensures configurations are easy to understand, maintain, and debug while providing clear feedback when issues arise.