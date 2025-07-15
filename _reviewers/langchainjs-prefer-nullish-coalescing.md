---
title: Prefer nullish coalescing
description: 'When handling null or undefined values, use modern JavaScript patterns
  to write more robust and maintainable code:


  1. Use the nullish coalescing operator (`??`) instead of logical OR (`||`) for defaults:'
repository: langchain-ai/langchainjs
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 15004
---

When handling null or undefined values, use modern JavaScript patterns to write more robust and maintainable code:

1. Use the nullish coalescing operator (`??`) instead of logical OR (`||`) for defaults:
```javascript
// Good: Only falls back when value is null or undefined
this.endpointUrl = fields.endpointUrl ?? getEnvironmentVariable("AZUREML_URL");

// Avoid: Will also replace empty strings, 0, and false
this.endpointUrl = fields.endpointUrl || getEnvironmentVariable("AZUREML_URL");
```

2. Conditionally include properties in objects only when they exist:
```javascript
// Good: Only adds the property when content exists
const options = {
  ...otherOptions,
  ...(message.content != null ? { content: formatContent(message.content) } : {})
};

// Avoid: Passing undefined values to APIs
const options = {
  ...otherOptions,
  audio: this.audio // might be undefined
};
```

3. Use strict equality (`===`, `!==`) for null checks:
```javascript
// Good: Clear intent, checks for both null and undefined
if (documents === null || documents === undefined) {
  // Handle the case
}
// Or more concisely:
if (documents == null) {
  // Handle the case
}
```

4. Thoroughly check combinations of conditions when handling nullable values:
```javascript
// Good: Raises an error only when both client and credentials are missing
if (!config.client && (!endpoint || !key)) {
  throw new Error("Missing required configuration");
}

// Avoid: Oversimplified check
if (!config.client && !endpoint && !key) {
  // This will only throw if ALL are missing
}
```

These patterns help prevent subtle bugs and make your code's intent clearer to other developers.
