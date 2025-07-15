---
title: Consistent AI naming
description: Use specific and consistent naming conventions when referencing AI services,
  models, and their parameters throughout your codebase. Always include the full provider
  name (e.g., "AzureOpenAI" instead of just "Azure") to clearly distinguish between
  different AI services and avoid ambiguity.
repository: langchain-ai/langchainjs
label: AI
language: JavaScript
comments_count: 3
repository_stars: 15004
---

Use specific and consistent naming conventions when referencing AI services, models, and their parameters throughout your codebase. Always include the full provider name (e.g., "AzureOpenAI" instead of just "Azure") to clearly distinguish between different AI services and avoid ambiguity.

For variables, parameters, and properties related to AI services:
- Use fully qualified names that precisely identify the AI provider and service
- Maintain naming consistency across configuration objects, function parameters, and component properties
- Follow established patterns in the codebase for similar AI integrations

Example:
```javascript
// Incorrect - ambiguous naming
const azureParams = `{
  azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
  azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
}`;

// Correct - specific and consistent naming
const azureOpenAIParams = `{
  azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
  azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
  openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"]
}`;

// Component property should also use the specific name
@property {boolean} [hideAzureOpenAI] - Whether or not to hide Microsoft Azure OpenAI chat model.
```

This practice improves code readability, reduces confusion when working with multiple AI services, and makes maintenance easier, especially as you integrate additional AI providers in the future.
