---
title: Defensive null checking
description: Always perform explicit null/undefined checks before accessing properties
  or using values that could be null or undefined. Use strict equality checks rather
  than relying on JavaScript's truthy/falsy evaluation which can lead to subtle bugs.
repository: aws/aws-sdk-js
label: Null Handling
language: JavaScript
comments_count: 7
repository_stars: 7628
---

Always perform explicit null/undefined checks before accessing properties or using values that could be null or undefined. Use strict equality checks rather than relying on JavaScript's truthy/falsy evaluation which can lead to subtle bugs.

Common patterns to adopt:
1. Check objects before accessing their properties:
   ```javascript
   // Bad:
   if (error.code === 'AuthorizationHeaderMalformed') { /* ... */ }
   
   // Good:
   if (error && error.code === 'AuthorizationHeaderMalformed') { /* ... */ }
   ```

2. Be careful with array index checks:
   ```javascript
   // Bad - indexOf returns 0 for first item which is falsy:
   if (list.indexOf(member)) { return true; }
   
   // Good:
   if (list.indexOf(member) >= 0) { return true; }
   ```

3. Use typeof checks before accessing browser/environment-specific objects:
   ```javascript
   // Bad:
   return window.localStorage !== null;
   
   // Good:
   return AWS.util.isBrowser() && window.localStorage !== null && typeof window.localStorage === 'object';
   ```

4. Provide defaults for parameters that could be undefined:
   ```javascript
   // Bad:
   function handleParams(params) {
     params.property = 'value'; // Fails if params is null/undefined
   }
   
   // Good:
   function handleParams(params) {
     params = params || {};
     params.property = 'value';
   }
   ```

5. Use type checks for numeric values instead of truthy checks:
   ```javascript
   // Bad - fails for zero values:
   if (params.$waiter.delay) {
     this.config.delay = params.$waiter.delay;
   }
   
   // Good:
   if (typeof params.$waiter.delay === 'number') {
     this.config.delay = params.$waiter.delay;
   }
   ```

Consistent null checking prevents the most common class of runtime errors and produces more predictable code.
