---
title: Document sdk version requirements
description: Always explicitly document AWS SDK version requirements in your project,
  and include configuration instructions for different deployment environments. This
  is especially critical for Lambda functions where the runtime may include its own
  SDK version.
repository: aws/aws-sdk-js
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 7628
---

Always explicitly document AWS SDK version requirements in your project, and include configuration instructions for different deployment environments. This is especially critical for Lambda functions where the runtime may include its own SDK version.

For Lambda deployments:
1. Specify whether you're using the bundled SDK or importing your own
2. Document the compatibility requirements clearly in your configuration files
3. Include references to runtime documentation when relevant

Example in a project README or configuration file:
```javascript
// AWS SDK Version requirements
// Current project requires: aws-sdk >= 2.466.0
// 
// If using Lambda:
// - Check runtime version: https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
// - If bundling your own SDK: npm install aws-sdk@latest
//   and follow https://docs.aws.amazon.com/lambda/latest/dg/nodejs-create-deployment-pkg.html
//
// For version verification in code:
const AWS = require("aws-sdk");
console.log("Using AWS SDK version:", AWS.VERSION);
```

This documentation helps prevent compatibility issues like "Unexpected key" errors and ensures all developers understand the environment configuration requirements.
