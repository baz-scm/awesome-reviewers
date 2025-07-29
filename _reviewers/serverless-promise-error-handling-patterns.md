---
title: Promise error handling patterns
description: When handling promise errors, use the second callback parameter of `.then()`
  instead of `.catch()` when you want to handle only the specific promise rejection
  and avoid accidentally catching programmer errors from the success handler. Use
  `.catch()` only when you intend to handle all errors in the promise chain.
repository: serverless/serverless
label: Error Handling
language: JavaScript
comments_count: 7
repository_stars: 46810
---

When handling promise errors, use the second callback parameter of `.then()` instead of `.catch()` when you want to handle only the specific promise rejection and avoid accidentally catching programmer errors from the success handler. Use `.catch()` only when you intend to handle all errors in the promise chain.

Additionally, use appropriate error types and provide meaningful context in error messages. Use `ServerlessError` for user configuration issues and regular `Error` for API/programming issues. Always include error codes for better monitoring and add relevant context like resource names to error messages.

Example of proper promise error handling:
```javascript
// Good - only catches errors from the specific promise
return this.provider.request('ApiGatewayV2', 'getApi', { ApiId: id })
  .then(result => {
    stackData.externalHttpApiEndpoint = result.ApiEndpoint;
  }, error => {
    throw new this.serverless.classes.Error(
      `Could not resolve provider.httpApi.id parameter. ${error.message}`,
      'HTTPAPI_ID_RESOLUTION_ERROR'
    );
  });

// Avoid - catches both promise rejection AND any errors in success handler
return this.provider.request('ApiGatewayV2', 'getApi', { ApiId: id })
  .then(result => {
    stackData.externalHttpApiEndpoint = result.ApiEndpoint;
  })
  .catch(error => {
    throw new this.serverless.classes.Error(
      `Could not resolve provider.httpApi.id parameter. ${error.message}`
    );
  });
```

This pattern prevents masking programmer errors while ensuring proper error context and appropriate error types for better debugging and monitoring.