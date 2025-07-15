---
title: Validate configurations with clarity
description: 'Configuration validation should use explicit checks and clear conditional
  logic to improve code readability and prevent errors. When validating configuration
  values:'
repository: aws/aws-sdk-js
label: Configurations
language: JavaScript
comments_count: 3
repository_stars: 7628
---

Configuration validation should use explicit checks and clear conditional logic to improve code readability and prevent errors. When validating configuration values:

1. Use explicit string comparisons for environment variables
2. Structure conditional logic clearly with early returns
3. Group related checks together
4. Use descriptive error messages

Example:
```javascript
// ❌ Avoid complex nested conditions
if (config.stsRegionalEndpoints) {
  if (typeof config.stsRegionalEndpoints === 'string') {
    if (['legacy', 'regional'].indexOf(config.stsRegionalEndpoints.toLowerCase()) >= 0) {
      // handle valid config
    } else {
      throw new Error('Invalid config');
    }
  }
}

// ✅ Use clear validation with early returns
function validateConfig(config) {
  if (!config.stsRegionalEndpoints) return;
  
  if (typeof config.stsRegionalEndpoints !== 'string') {
    throw new Error('stsRegionalEndpoints must be a string');
  }

  const validValues = ['legacy', 'regional'];
  if (!validValues.includes(config.stsRegionalEndpoints.toLowerCase())) {
    throw new Error('stsRegionalEndpoints must be either "legacy" or "regional"');
  }

  // proceed with valid config
}
```
