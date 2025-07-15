---
title: Platform-appropriate environment variables
description: Always use the correct syntax for accessing environment variables based
  on the target platform. In JavaScript/Node.js environments, use `process.env.VARIABLE_NAME`
  instead of syntaxes from other languages (e.g., Python's `os.environ`).
repository: langchain-ai/langchainjs
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 15004
---

Always use the correct syntax for accessing environment variables based on the target platform. In JavaScript/Node.js environments, use `process.env.VARIABLE_NAME` instead of syntaxes from other languages (e.g., Python's `os.environ`).

Example:
```javascript
// Incorrect - Using Python syntax in JavaScript
const config = {
  azure_endpoint: os.environ["AZURE_OPENAI_ENDPOINT"],
  azure_deployment: os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
  openai_api_version: os.environ["AZURE_OPENAI_API_VERSION"]
};

// Correct - Using JavaScript syntax
const config = {
  azure_endpoint: process.env.AZURE_OPENAI_ENDPOINT,
  azure_deployment: process.env.AZURE_OPENAI_DEPLOYMENT_NAME,
  openai_api_version: process.env.AZURE_OPENAI_API_VERSION
};
```

For platform-specific configurations, consider using appropriate file formats (like .mdx for Node-specific code) or implement automatic import methods that work across environments to improve compatibility.
