---
title: Early return after errors
description: When handling errors in asynchronous functions, always return immediately
  after invoking a callback with an error to prevent subsequent code execution. This
  avoids the risk of calling callbacks multiple times or continuing execution paths
  that assume success.
repository: aws/aws-sdk-js
label: Error Handling
language: JavaScript
comments_count: 6
repository_stars: 7628
---

When handling errors in asynchronous functions, always return immediately after invoking a callback with an error to prevent subsequent code execution. This avoids the risk of calling callbacks multiple times or continuing execution paths that assume success.

Bad pattern:
```javascript
function loadViaCredentialProcess(profile, callback) {
  proc.exec(profile['credential_process'], function(err, stdOut, stdErr) {
    if (err) {
      callback(err, null);
    }
    // Problem: execution continues even after error callback
    try {
      var credData = JSON.parse(stdOut);
      // More processing that might fail or call callback again
      callback(null, credData);
    } catch(e) {
      callback(e);
    }
  });
}
```

Good pattern:
```javascript
function loadViaCredentialProcess(profile, callback) {
  proc.exec(profile['credential_process'], function(err, stdOut, stdErr) {
    if (err) {
      return callback(err, null); // Return immediately after error callback
    }
    try {
      var credData = JSON.parse(stdOut);
      // More processing that only happens on success path
      callback(null, credData);
    } catch(e) {
      return callback(e); // Return after error in try/catch as well
    }
  });
}
```

For functions that can be called synchronously or asynchronously:
```javascript
function createPresignedPost(params, callback) {
  if (typeof params === 'function' && callback === undefined) {
    callback = params;
    params = null;
  }
  
  // Check for errors first, return early
  if (!this.config.credentials) {
    var error = new Error('No credentials');
    if (callback) {
      return callback(error);
    }
    throw error; // Throw for synchronous callers
  }
  
  // Success path only executes if no errors were found
  var result = this.finalizePost();
  return callback ? callback(null, result) : result;
}
```

This pattern creates clear separation between error and success paths, making code more maintainable and preventing hard-to-debug issues caused by multiple callback invocations or unexpected execution after errors.
