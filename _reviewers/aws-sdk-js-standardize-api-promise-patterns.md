---
title: Standardize API promise patterns
description: When adding promise support to API methods, implement a consistent pattern
  that handles both callback-style and multi-parameter methods. Use a standardized
  promisification approach that appends the promise-determining callback as the last
  argument.
repository: aws/aws-sdk-js
label: API
language: JavaScript
comments_count: 2
repository_stars: 7628
---

When adding promise support to API methods, implement a consistent pattern that handles both callback-style and multi-parameter methods. Use a standardized promisification approach that appends the promise-determining callback as the last argument.

Example implementation:
```javascript
function promisifyMethod(methodName, PromiseDependency) {
    return function promise() {
        var self = this;
        var args = Array.prototype.slice.call(arguments);
        return new PromiseDependency(function(resolve, reject) {
            args.push(function(err, data) {
                if (err) {
                    reject(err);
                } else {
                    resolve(data);
                }
            });
            self[methodName].apply(self, args);
        });
    };
}
```

This pattern ensures:
- Consistent promise behavior across all API methods
- Support for both simple callback methods and multi-parameter methods
- Proper error handling and promise rejection
- Compatibility with different promise implementations
