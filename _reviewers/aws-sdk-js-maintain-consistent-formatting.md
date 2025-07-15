---
title: Maintain consistent formatting
description: 'Enhance code readability and maintainability by applying consistent
  formatting practices throughout your codebase:


  1. Properly indent continuation lines (lines that are part of the same statement
  as the preceding line)'
repository: aws/aws-sdk-js
label: Code Style
language: JavaScript
comments_count: 4
repository_stars: 7628
---

Enhance code readability and maintainability by applying consistent formatting practices throughout your codebase:

1. Properly indent continuation lines (lines that are part of the same statement as the preceding line)
2. Separate logical blocks like test suites or function definitions with empty lines
3. Structure complex conditionals for readability

For complex conditionals, prefer nested if statements over lengthy, hard-to-parse single-line conditions:

```javascript
// Hard to read:
if ((AWS.HttpClient.streamsApiVersion !== 2) ||
  (!(operation.hasEventOutput && service.successfulResponse(resp)) &&
  (!stream || !stream.didCallback)))

// More readable:
if (!stream || !stream.didCallback) {
  // don't concat response chunks when using event streams unless response is unsuccessful
  if ((AWS.HttpClient.streamsApiVersion === 2) && operation.hasEventOutput && service.successfulResponse(resp)) {
    return;
  }
  // proceed with regular processing
}
```

Consistent formatting makes code easier to scan, understand, and maintain, reducing the cognitive load for everyone working with the codebase.
