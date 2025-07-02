---
title: Early return after errors
description: When handling errors in asynchronous functions, always return immediately
  after invoking a callback with an error to prevent subsequent code execution. This
  avoids the risk of calling callbacks multiple times or continuing execution paths
  that assume success.
repository: aws/aws-sdk-js
label: Error Handling
language: Javascript
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


[
  {
    "discussion_id": "127803453",
    "pr_number": 1631,
    "pr_file": "lib/request.js",
    "created_at": "2017-07-17T19:34:30+00:00",
    "commented_code": "*     request.send();\n   */\n  send: function send(callback) {\n    this.preventMultipleCalls();\n    if (callback) {\n      // append to user agent\n      this.httpRequest.appendToUserAgent('callback');\n      this.on('complete', function (resp) {\n        callback.call(resp, resp.error, resp.data);\n      });\n    }\n    this._didSend = true;\n    this.runTo();\n\n    return this.response;\n  },\n\n  /**\n   * @api private\n   */\n  preventMultipleCalls: function preventMultipleCalls() {",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "127803453",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1631,
        "pr_file": "lib/request.js",
        "discussion_id": "127803453",
        "commented_code": "@@ -357,19 +357,34 @@ AWS.Request = inherit({\n    *     request.send();\n    */\n   send: function send(callback) {\n+    this.preventMultipleCalls();\n     if (callback) {\n       // append to user agent\n       this.httpRequest.appendToUserAgent('callback');\n       this.on('complete', function (resp) {\n         callback.call(resp, resp.error, resp.data);\n       });\n     }\n+    this._didSend = true;\n     this.runTo();\n \n     return this.response;\n   },\n \n   /**\n+   * @api private\n+   */\n+  preventMultipleCalls: function preventMultipleCalls() {",
        "comment_created_at": "2017-07-17T19:34:30+00:00",
        "comment_author": "jeskew",
        "comment_body": "Maybe instead of throwing, this method could take a callback? That would allow the RequestAlreadyTriggeredError to be handled by user callbacks when `send` is called or emitted onto streams when `createReadStream` is called.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "101647511",
    "pr_number": 1350,
    "pr_file": "lib/services/s3.js",
    "created_at": "2017-02-16T22:51:15+00:00",
    "commented_code": "return request.presign(expires, callback);\n  },\n\n\n  /**\n   * Get a pre-signed POST policy for a given operation name.\n   *\n   * @param params [map]\n   * @option params.Bucket [String]\n   * @option params.Expires [Number]\n   * @option params.Conditions [Array]\n   * @option params.Fields [map]\n   * @param callback [Function]\n   *\n   * @note All fields passed in when creating presigned post data will be signed\n   *   as exact match conditions. Any fields that will be interpolated by S3\n   *   must be added to the fields hash after signing, and an appropriate\n   *   condition for such fields must be explicitly added to the Conditions\n   *   array passed to this function before signing.\n   *\n   * @example Presiging post data with a known key\n   *   var params = {\n   *     Bucket: 'bucket',\n   *     Fields: {\n   *       key: 'key'\n   *     }\n   *   };\n   *   s3.createPresignedPost(params, function(err, data) {\n   *     if (err) {\n   *       console.error('Presigning post data encountered an error', err);\n   *     } else {\n   *       console.log('The post data is', data);\n   *     }\n   *   });\n   *\n   * @example Presigning post data with an interpolated key\n   *   var params = {\n   *     Bucket: 'bucket',\n   *     Conditions: [\n   *       ['starts-with', '$key', 'path/to/uploads/']\n   *     ]\n   *   };\n   *   s3.createPresignedPost(params, function(err, data) {\n   *     if (err) {\n   *       console.error('Presigning post data encountered an error', err);\n   *     } else {\n   *       data.Fields.key = 'path/to/uploads/${filename}';\n   *       console.log('The post data is', data);\n   *     }\n   *   });\n   *\n   * @note You must ensure that you have static or previously resolved\n   *   credentials if you call this method synchronously (with no callback),\n   *   otherwise it may not properly sign the request. If you cannot guarantee\n   *   this (you are using an asynchronous credential provider, i.e., EC2\n   *   IAM roles), you should always call this method with an asynchronous\n   *   callback.\n   */\n  createPresignedPost: function createPresignedPost(params, callback) {\n    if (typeof params === 'function' && callback === undefined) {\n      callback = params;\n      params = null;\n    }\n\n    params = AWS.util.copy(params || {});\n    var boundParams = this.config.params || {};\n    var bucket = params.Bucket || boundParams.Bucket,\n      self = this,\n      config = this.config,\n      endpoint = AWS.util.copy(this.endpoint);\n    if (!config.s3BucketEndpoint) {\n      endpoint.pathname = '/' + bucket;\n    }\n\n    function finalizePost() {",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "101647511",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1350,
        "pr_file": "lib/services/s3.js",
        "discussion_id": "101647511",
        "commented_code": "@@ -731,6 +731,173 @@ AWS.util.update(AWS.S3.prototype, {\n     return request.presign(expires, callback);\n   },\n \n+\n+  /**\n+   * Get a pre-signed POST policy for a given operation name.\n+   *\n+   * @param params [map]\n+   * @option params.Bucket [String]\n+   * @option params.Expires [Number]\n+   * @option params.Conditions [Array]\n+   * @option params.Fields [map]\n+   * @param callback [Function]\n+   *\n+   * @note All fields passed in when creating presigned post data will be signed\n+   *   as exact match conditions. Any fields that will be interpolated by S3\n+   *   must be added to the fields hash after signing, and an appropriate\n+   *   condition for such fields must be explicitly added to the Conditions\n+   *   array passed to this function before signing.\n+   *\n+   * @example Presiging post data with a known key\n+   *   var params = {\n+   *     Bucket: 'bucket',\n+   *     Fields: {\n+   *       key: 'key'\n+   *     }\n+   *   };\n+   *   s3.createPresignedPost(params, function(err, data) {\n+   *     if (err) {\n+   *       console.error('Presigning post data encountered an error', err);\n+   *     } else {\n+   *       console.log('The post data is', data);\n+   *     }\n+   *   });\n+   *\n+   * @example Presigning post data with an interpolated key\n+   *   var params = {\n+   *     Bucket: 'bucket',\n+   *     Conditions: [\n+   *       ['starts-with', '$key', 'path/to/uploads/']\n+   *     ]\n+   *   };\n+   *   s3.createPresignedPost(params, function(err, data) {\n+   *     if (err) {\n+   *       console.error('Presigning post data encountered an error', err);\n+   *     } else {\n+   *       data.Fields.key = 'path/to/uploads/${filename}';\n+   *       console.log('The post data is', data);\n+   *     }\n+   *   });\n+   *\n+   * @note You must ensure that you have static or previously resolved\n+   *   credentials if you call this method synchronously (with no callback),\n+   *   otherwise it may not properly sign the request. If you cannot guarantee\n+   *   this (you are using an asynchronous credential provider, i.e., EC2\n+   *   IAM roles), you should always call this method with an asynchronous\n+   *   callback.\n+   */\n+  createPresignedPost: function createPresignedPost(params, callback) {\n+    if (typeof params === 'function' && callback === undefined) {\n+      callback = params;\n+      params = null;\n+    }\n+\n+    params = AWS.util.copy(params || {});\n+    var boundParams = this.config.params || {};\n+    var bucket = params.Bucket || boundParams.Bucket,\n+      self = this,\n+      config = this.config,\n+      endpoint = AWS.util.copy(this.endpoint);\n+    if (!config.s3BucketEndpoint) {\n+      endpoint.pathname = '/' + bucket;\n+    }\n+\n+    function finalizePost() {",
        "comment_created_at": "2017-02-16T22:51:15+00:00",
        "comment_author": "chrisradek",
        "comment_body": "It doesn't seem like there's a need for this function. Couldn't you store the return value directly in an object, then pass that to the callback/return it?",
        "pr_file_module": null
      },
      {
        "comment_id": "101667755",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1350,
        "pr_file": "lib/services/s3.js",
        "discussion_id": "101647511",
        "commented_code": "@@ -731,6 +731,173 @@ AWS.util.update(AWS.S3.prototype, {\n     return request.presign(expires, callback);\n   },\n \n+\n+  /**\n+   * Get a pre-signed POST policy for a given operation name.\n+   *\n+   * @param params [map]\n+   * @option params.Bucket [String]\n+   * @option params.Expires [Number]\n+   * @option params.Conditions [Array]\n+   * @option params.Fields [map]\n+   * @param callback [Function]\n+   *\n+   * @note All fields passed in when creating presigned post data will be signed\n+   *   as exact match conditions. Any fields that will be interpolated by S3\n+   *   must be added to the fields hash after signing, and an appropriate\n+   *   condition for such fields must be explicitly added to the Conditions\n+   *   array passed to this function before signing.\n+   *\n+   * @example Presiging post data with a known key\n+   *   var params = {\n+   *     Bucket: 'bucket',\n+   *     Fields: {\n+   *       key: 'key'\n+   *     }\n+   *   };\n+   *   s3.createPresignedPost(params, function(err, data) {\n+   *     if (err) {\n+   *       console.error('Presigning post data encountered an error', err);\n+   *     } else {\n+   *       console.log('The post data is', data);\n+   *     }\n+   *   });\n+   *\n+   * @example Presigning post data with an interpolated key\n+   *   var params = {\n+   *     Bucket: 'bucket',\n+   *     Conditions: [\n+   *       ['starts-with', '$key', 'path/to/uploads/']\n+   *     ]\n+   *   };\n+   *   s3.createPresignedPost(params, function(err, data) {\n+   *     if (err) {\n+   *       console.error('Presigning post data encountered an error', err);\n+   *     } else {\n+   *       data.Fields.key = 'path/to/uploads/${filename}';\n+   *       console.log('The post data is', data);\n+   *     }\n+   *   });\n+   *\n+   * @note You must ensure that you have static or previously resolved\n+   *   credentials if you call this method synchronously (with no callback),\n+   *   otherwise it may not properly sign the request. If you cannot guarantee\n+   *   this (you are using an asynchronous credential provider, i.e., EC2\n+   *   IAM roles), you should always call this method with an asynchronous\n+   *   callback.\n+   */\n+  createPresignedPost: function createPresignedPost(params, callback) {\n+    if (typeof params === 'function' && callback === undefined) {\n+      callback = params;\n+      params = null;\n+    }\n+\n+    params = AWS.util.copy(params || {});\n+    var boundParams = this.config.params || {};\n+    var bucket = params.Bucket || boundParams.Bucket,\n+      self = this,\n+      config = this.config,\n+      endpoint = AWS.util.copy(this.endpoint);\n+    if (!config.s3BucketEndpoint) {\n+      endpoint.pathname = '/' + bucket;\n+    }\n+\n+    function finalizePost() {",
        "comment_created_at": "2017-02-17T01:17:01+00:00",
        "comment_author": "jeskew",
        "comment_body": "This function should only be invoked once credentials have been resolved, so it needs to be called from the callback.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "115840969",
    "pr_number": 1507,
    "pr_file": "test/request.spec.js",
    "created_at": "2017-05-10T20:14:30+00:00",
    "commented_code": "s = request.createReadStream();\n        s.on('error', function(e) {\n          error = e;\n          expect(error).to.be[\"null\"];\n          expect(error).to.not.be[\"null\"];\n        });\n        s.on('data', function(c) {\n          return data += c.toString();\n        });\n        return s.on('end', function() {\n          expect(error).to.be[\"null\"];\n          expect(data).to.equal('FOOBARBAZQU');\n          expect(error).to.not.be[\"null\"];",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "115840969",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1507,
        "pr_file": "test/request.spec.js",
        "discussion_id": "115840969",
        "commented_code": "@@ -758,14 +758,13 @@ describe('AWS.Request', function() {\n         s = request.createReadStream();\n         s.on('error', function(e) {\n           error = e;\n-          expect(error).to.be[\"null\"];\n+          expect(error).to.not.be[\"null\"];\n         });\n         s.on('data', function(c) {\n           return data += c.toString();\n         });\n         return s.on('end', function() {\n-          expect(error).to.be[\"null\"];\n-          expect(data).to.equal('FOOBARBAZQU');\n+          expect(error).to.not.be[\"null\"];",
        "comment_created_at": "2017-05-10T20:14:30+00:00",
        "comment_author": "jeskew",
        "comment_body": "Is this a breaking change? Previously, users would get up to `content-length` bytes and no more if the returned stream exceeded that length; now, the stream will emit an error event in that case. Was there ever a case where `content-length` would be wrong but the user was OK with receiving a truncated stream?",
        "pr_file_module": null
      },
      {
        "comment_id": "115843940",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1507,
        "pr_file": "test/request.spec.js",
        "discussion_id": "115840969",
        "commented_code": "@@ -758,14 +758,13 @@ describe('AWS.Request', function() {\n         s = request.createReadStream();\n         s.on('error', function(e) {\n           error = e;\n-          expect(error).to.be[\"null\"];\n+          expect(error).to.not.be[\"null\"];\n         });\n         s.on('data', function(c) {\n           return data += c.toString();\n         });\n         return s.on('end', function() {\n-          expect(error).to.be[\"null\"];\n-          expect(data).to.equal('FOOBARBAZQU');\n+          expect(error).to.not.be[\"null\"];",
        "comment_created_at": "2017-05-10T20:27:58+00:00",
        "comment_author": "chrisradek",
        "comment_body": "I don't think giving the user a truncated stream is really ok. I think this test was checking the behavior the SDK exhibited, rather than what was intended.\r\n\r\n[Here](https://github.com/aws/aws-sdk-js/blob/master/lib/request.js#L606-L611), there's a check to see if the incoming data matched the content-length. It should be throwing an error when the content-length is less than the data received. When I was testing though, I discovered that when the body is larger than the content-length, node throws a `ParseError`. However, because we were swallowing these errors (due to already receiving response headers), and node.js still gave us access to the body up to the content-length, it appeared as though we could never detect when data streamed in exceeded the expected amount.",
        "pr_file_module": null
      },
      {
        "comment_id": "115852151",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1507,
        "pr_file": "test/request.spec.js",
        "discussion_id": "115840969",
        "commented_code": "@@ -758,14 +758,13 @@ describe('AWS.Request', function() {\n         s = request.createReadStream();\n         s.on('error', function(e) {\n           error = e;\n-          expect(error).to.be[\"null\"];\n+          expect(error).to.not.be[\"null\"];\n         });\n         s.on('data', function(c) {\n           return data += c.toString();\n         });\n         return s.on('end', function() {\n-          expect(error).to.be[\"null\"];\n-          expect(data).to.equal('FOOBARBAZQU');\n+          expect(error).to.not.be[\"null\"];",
        "comment_created_at": "2017-05-10T21:02:51+00:00",
        "comment_author": "jeskew",
        "comment_body": "I can't imagine that the data received up to `content-length` would be usable in most cases... you would end up with an unparsable partial XML or JSON document unless the service was returning a byte stream. I think the change in this PR is correct, but we should be on the lookout for issues where users were receiving partial byte streams and are now encountering stream errors.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "181819271",
    "pr_number": 1956,
    "pr_file": "lib/http/response-validator/integrityChecker.js",
    "created_at": "2018-04-16T17:14:35+00:00",
    "commented_code": "this.providedChecksum.length !== CHECKSUM_BYTE_LEN ||\n    this.hash.digest('base64') !== this.providedChecksum.toString('base64')\n  ) {\n    this.emit('error', AWS.util.error(\n    callback( AWS.util.error(\n      new Error('Response fails integrity check.'),\n      { code: 'ResponseChecksumMismatch' })\n    );\n    )",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "181819271",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1956,
        "pr_file": "lib/http/response-validator/integrityChecker.js",
        "discussion_id": "181819271",
        "commented_code": "@@ -53,10 +48,10 @@ IntegrityCheckerStream.prototype._flush = function(callback) {\n     this.providedChecksum.length !== CHECKSUM_BYTE_LEN ||\n     this.hash.digest('base64') !== this.providedChecksum.toString('base64')\n   ) {\n-    this.emit('error', AWS.util.error(\n+    callback( AWS.util.error(\n       new Error('Response fails integrity check.'),\n       { code: 'ResponseChecksumMismatch' })\n-    );\n+    )",
        "comment_created_at": "2018-04-16T17:14:35+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Call `return` either on the same line as `callback` or right under. Right now `callback` might be triggered twice: once with an error and then once without an error a couple lines below.",
        "pr_file_module": null
      },
      {
        "comment_id": "181866700",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1956,
        "pr_file": "lib/http/response-validator/integrityChecker.js",
        "discussion_id": "181819271",
        "commented_code": "@@ -53,10 +48,10 @@ IntegrityCheckerStream.prototype._flush = function(callback) {\n     this.providedChecksum.length !== CHECKSUM_BYTE_LEN ||\n     this.hash.digest('base64') !== this.providedChecksum.toString('base64')\n   ) {\n-    this.emit('error', AWS.util.error(\n+    callback( AWS.util.error(\n       new Error('Response fails integrity check.'),\n       { code: 'ResponseChecksumMismatch' })\n-    );\n+    )",
        "comment_created_at": "2018-04-16T20:00:48+00:00",
        "comment_author": "AllanZhengYP",
        "comment_body": "Here calling callback twice won't actually write anything to stream. I will fix it though",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "265312860",
    "pr_number": 2559,
    "pr_file": "lib/credentials/shared_ini_file_credentials.js",
    "created_at": "2019-03-13T20:15:45+00:00",
    "commented_code": "* @param profile [map] credentials profile\n  * @throws SharedIniFileCredentialsProviderFailure\n  */\n  loadViaCredentialProcess: function loadCredentialProcess(profile, callback) {\n    try {\n      var output = proc.execSync(profile['credential_process']);\n      var credData = JSON.parse(output);\n      if (parseInt(credData.Version) !== 1) {\n        throw AWS.util.error(\n          Error('credential_process does not return Version == 1 for profile ' + this.profile),\n          { code: 'SharedIniFileCredentialsProviderFailure'}\n loadViaCredentialProcess: function loadViaCredentialProcess(profile, callback) {\n  proc.exec(profile['credential_process'], function(err,stdOut, stdErr) {\n    if (err) {\n      callback(err, null);\n    } else if (stdErr) {\n      callback(stdErr, null);",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "265312860",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 2559,
        "pr_file": "lib/credentials/shared_ini_file_credentials.js",
        "discussion_id": "265312860",
        "commented_code": "@@ -187,25 +200,33 @@ AWS.SharedIniFileCredentials = AWS.util.inherit(AWS.Credentials, {\n   * @param profile [map] credentials profile\n   * @throws SharedIniFileCredentialsProviderFailure\n   */\n-  loadViaCredentialProcess: function loadCredentialProcess(profile, callback) {\n-    try {\n-      var output = proc.execSync(profile['credential_process']);\n-      var credData = JSON.parse(output);\n-      if (parseInt(credData.Version) !== 1) {\n-        throw AWS.util.error(\n-          Error('credential_process does not return Version == 1 for profile ' + this.profile),\n-          { code: 'SharedIniFileCredentialsProviderFailure'}\n+ loadViaCredentialProcess: function loadViaCredentialProcess(profile, callback) {\n+  proc.exec(profile['credential_process'], function(err,stdOut, stdErr) {\n+    if (err) {\n+      callback(err, null);\n+    } else if (stdErr) {\n+      callback(stdErr, null);",
        "comment_created_at": "2019-03-13T20:15:45+00:00",
        "comment_author": "jstewmon",
        "comment_body": "stderr is often used for ancillary information (like a deprecation warning) even when the command succeeds, so I would advise against treating a truthy value as a failure.\r\n\r\nFWIW, the [botocore implementation] ignores stderr.\r\n\r\nIf this is retained, I suggest passing `AWS.util.error(new Error(stdErr), {code: 'SharedIniCredentialsProviderFailue'})`, so that the callback receives a normalized `Error`, not a `string`.\r\n\r\n[botocore implementation]: https://github.com/boto/botocore/blob/8d3ea0e61473fba43774eb3c74e1b22995ee7370/botocore/credentials.py#L804-L833",
        "pr_file_module": null
      },
      {
        "comment_id": "265324515",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 2559,
        "pr_file": "lib/credentials/shared_ini_file_credentials.js",
        "discussion_id": "265312860",
        "commented_code": "@@ -187,25 +200,33 @@ AWS.SharedIniFileCredentials = AWS.util.inherit(AWS.Credentials, {\n   * @param profile [map] credentials profile\n   * @throws SharedIniFileCredentialsProviderFailure\n   */\n-  loadViaCredentialProcess: function loadCredentialProcess(profile, callback) {\n-    try {\n-      var output = proc.execSync(profile['credential_process']);\n-      var credData = JSON.parse(output);\n-      if (parseInt(credData.Version) !== 1) {\n-        throw AWS.util.error(\n-          Error('credential_process does not return Version == 1 for profile ' + this.profile),\n-          { code: 'SharedIniFileCredentialsProviderFailure'}\n+ loadViaCredentialProcess: function loadViaCredentialProcess(profile, callback) {\n+  proc.exec(profile['credential_process'], function(err,stdOut, stdErr) {\n+    if (err) {\n+      callback(err, null);\n+    } else if (stdErr) {\n+      callback(stdErr, null);",
        "comment_created_at": "2019-03-13T20:47:32+00:00",
        "comment_author": "srchase",
        "comment_body": "Followed the botocore implementation and ignored stderr. thanks!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "268204892",
    "pr_number": 2559,
    "pr_file": "lib/credentials/process_credentials.js",
    "created_at": "2019-03-22T14:56:10+00:00",
    "commented_code": "var AWS = require('../core');\nvar proc = require('child_process');\nvar iniLoader = AWS.util.iniLoader;\n\n/**\n * Represents credentials loaded from shared credentials file\n * (defaulting to ~/.aws/credentials or defined by the\n * `AWS_SHARED_CREDENTIALS_FILE` environment variable).\n *\n * ## Using process credentials\n *\n * The credentials file can specify a credential provider that executes\n * a given process and attempts to read its stdout to recieve a JSON payload\n * containing the credentials:\n *\n *     [default]\n *     credential_process = /usr/bin/credential_proc\n *\n * Automatically handles refreshing credentials if an Expiration time is\n * provided in the credentials payload. Credentials supplied in the same profile\n * will take precedence over the credential_process.\n *\n * Sourcing credentials from an external process can potentially be dangerous,\n * so proceed with caution. Other credential providers should be preferred if\n * at all possible. If using this option, you should make sure that the shared\n * credentials file is as locked down as possible using security best practices\n * for your operating system.\n *\n * ## Using custom profiles\n *\n * The SDK supports loading credentials for separate profiles. This can be done\n * in two ways:\n *\n * 1. Set the `AWS_PROFILE` environment variable in your process prior to\n *    loading the SDK.\n * 2. Directly load the AWS.ProcessCredentials provider:\n *\n * ```javascript\n * var creds = new AWS.ProcessCredentials({profile: 'myprofile'});\n * AWS.config.credentials = creds;\n * ```\n *\n * @!macro nobrowser\n */\nAWS.ProcessCredentials = AWS.util.inherit(AWS.Credentials, {\n  /**\n   * Creates a new ProcessCredentials object.\n   *\n   * @param options [map] a set of options\n   * @option options profile [String] (AWS_PROFILE env var or 'default')\n   *   the name of the profile to load.\n   * @option options filename [String] ('~/.aws/credentials' or defined by\n   *   AWS_SHARED_CREDENTIALS_FILE process env var)\n   *   the filename to use when loading credentials.\n   * @option options callback [Function] (err) Credentials are eagerly loaded\n   *   by the constructor. When the callback is called with no error, the\n   *   credentials have been loaded successfully.\n   * @option options httpOptions [map] A set of options to pass to the low-level\n   *   HTTP request. Currently supported options are:\n   *   * **proxy** [String] &mdash; the URL to proxy requests through\n   *   * **agent** [http.Agent, https.Agent] &mdash; the Agent object to perform\n   *     HTTP requests with. Used for connection pooling. Defaults to the global\n   *     agent (`http.globalAgent`) for non-SSL connections. Note that for\n   *     SSL connections, a special Agent object is used in order to enable\n   *     peer certificate verification. This feature is only available in the\n   *     Node.js environment.\n   *   * **connectTimeout** [Integer] &mdash; Sets the socket to timeout after\n   *     failing to establish a connection with the server after\n   *     `connectTimeout` milliseconds. This timeout has no effect once a socket\n   *     connection has been established.\n   *   * **timeout** [Integer] &mdash; Sets the socket to timeout after timeout\n   *     milliseconds of inactivity on the socket. Defaults to two minutes\n   *     (120000).\n   *   * **xhrAsync** [Boolean] &mdash; Whether the SDK will send asynchronous\n   *     HTTP requests. Used in the browser environment only. Set to false to\n   *     send requests synchronously. Defaults to true (async on).\n   *   * **xhrWithCredentials** [Boolean] &mdash; Sets the \"withCredentials\"\n   *     property of an XMLHttpRequest object. Used in the browser environment\n   *     only. Defaults to false.\n   */\n  constructor: function ProcessCredentials(options) {\n    AWS.Credentials.call(this);\n\n    options = options || {};\n\n    this.filename = options.filename;\n    this.profile = options.profile || process.env.AWS_PROFILE || AWS.util.defaultProfile;\n    this.httpOptions = options.httpOptions || null;\n    this.get(options.callback || AWS.util.fn.noop);\n  },\n\n  /**\n   * @api private\n   */\n  load: function load(callback) {\n    var self = this;\n    try {\n      var profiles = {};\n      var profilesFromConfig = {};\n      if (process.env[AWS.util.configOptInEnv]) {\n        var profilesFromConfig = iniLoader.loadFrom({\n          isConfig: true,\n          filename: process.env[AWS.util.sharedConfigFileEnv]\n        });\n      }\n      var profilesFromCreds = iniLoader.loadFrom({\n        filename: this.filename ||\n          (process.env[AWS.util.configOptInEnv] && process.env[AWS.util.sharedCredentialsFileEnv])\n      });\n      for (var i = 0, profileNames = Object.keys(profilesFromCreds); i < profileNames.length; i++) {\n        profiles[profileNames[i]] = profilesFromCreds[profileNames[i]];\n      }\n      // load after profilesFromCreds to prefer profilesFromConfig\n      for (var i = 0, profileNames = Object.keys(profilesFromConfig); i < profileNames.length; i++) {\n        profiles[profileNames[i]] = profilesFromConfig[profileNames[i]];\n      }\n      var profile = profiles[this.profile] || {};\n\n      if (Object.keys(profile).length === 0) {\n        throw AWS.util.error(\n          new Error('Profile ' + this.profile + ' not found'),\n          { code: 'ProcessCredentialsProviderFailure' }\n        );\n      }\n\n      if (profile['credential_process']) {\n        this.loadViaCredentialProcess(profile, function(err, data) {\n          if (err) {\n            callback(err, null);\n          } else {\n            self.expired = false;\n            self.accessKeyId = data.AccessKeyId;\n            self.secretAccessKey = data.SecretAccessKey;\n            self.sessionToken = data.SessionToken;\n            if (data.Expiration) {\n              self.expireTime = new Date(data.Expiration);\n            }\n            callback(null);\n          }\n        });\n      } else {\n        throw AWS.util.error(\n          new Error('Profile ' + this.profile + ' did not include credential process'),\n          { code: 'ProcessCredentialsProviderFailure' }\n        );\n      }\n      this.expired = false;\n      if (this.accessKeyId && this.secretAccessKey) {\n        callback(null);\n      }\n    } catch (err) {\n      callback(err);\n    }\n  },\n\n  /**\n  * Executes the credential_process and retrieves\n  * credentials from the output\n  * @api private\n  * @param profile [map] credentials profile\n  * @throws SharedIniFileCredentialsProviderFailure\n  */\n  loadViaCredentialProcess: function loadViaCredentialProcess(profile, callback) {\n    proc.exec(profile['credential_process'], function(err,stdOut, stdErr) {\n      try {\n        var credData = JSON.parse(stdOut);\n        if (credData.Expiration) {\n          var currentTime = AWS.util.date.getDate();\n          var expireTime = new Date(credData.Expiration);\n          if (expireTime < currentTime) {\n            err = AWS.util.error(\n              new Error('credential_process returned expired credentials'),\n              { code: 'ProcessCredentialsProviderFailure' }\n            );\n          }\n        } else if (credData.Version !== 1) {\n          err = AWS.util.error(\n            new Error('credential_process does not return Version == 1'),\n          { code: 'ProcessCredentialsProviderFailure' }\n          );\n        }\n        if (err) {",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "268204892",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 2559,
        "pr_file": "lib/credentials/process_credentials.js",
        "discussion_id": "268204892",
        "commented_code": "@@ -0,0 +1,206 @@\n+var AWS = require('../core');\n+var proc = require('child_process');\n+var iniLoader = AWS.util.iniLoader;\n+\n+/**\n+ * Represents credentials loaded from shared credentials file\n+ * (defaulting to ~/.aws/credentials or defined by the\n+ * `AWS_SHARED_CREDENTIALS_FILE` environment variable).\n+ *\n+ * ## Using process credentials\n+ *\n+ * The credentials file can specify a credential provider that executes\n+ * a given process and attempts to read its stdout to recieve a JSON payload\n+ * containing the credentials:\n+ *\n+ *     [default]\n+ *     credential_process = /usr/bin/credential_proc\n+ *\n+ * Automatically handles refreshing credentials if an Expiration time is\n+ * provided in the credentials payload. Credentials supplied in the same profile\n+ * will take precedence over the credential_process.\n+ *\n+ * Sourcing credentials from an external process can potentially be dangerous,\n+ * so proceed with caution. Other credential providers should be preferred if\n+ * at all possible. If using this option, you should make sure that the shared\n+ * credentials file is as locked down as possible using security best practices\n+ * for your operating system.\n+ *\n+ * ## Using custom profiles\n+ *\n+ * The SDK supports loading credentials for separate profiles. This can be done\n+ * in two ways:\n+ *\n+ * 1. Set the `AWS_PROFILE` environment variable in your process prior to\n+ *    loading the SDK.\n+ * 2. Directly load the AWS.ProcessCredentials provider:\n+ *\n+ * ```javascript\n+ * var creds = new AWS.ProcessCredentials({profile: 'myprofile'});\n+ * AWS.config.credentials = creds;\n+ * ```\n+ *\n+ * @!macro nobrowser\n+ */\n+AWS.ProcessCredentials = AWS.util.inherit(AWS.Credentials, {\n+  /**\n+   * Creates a new ProcessCredentials object.\n+   *\n+   * @param options [map] a set of options\n+   * @option options profile [String] (AWS_PROFILE env var or 'default')\n+   *   the name of the profile to load.\n+   * @option options filename [String] ('~/.aws/credentials' or defined by\n+   *   AWS_SHARED_CREDENTIALS_FILE process env var)\n+   *   the filename to use when loading credentials.\n+   * @option options callback [Function] (err) Credentials are eagerly loaded\n+   *   by the constructor. When the callback is called with no error, the\n+   *   credentials have been loaded successfully.\n+   * @option options httpOptions [map] A set of options to pass to the low-level\n+   *   HTTP request. Currently supported options are:\n+   *   * **proxy** [String] &mdash; the URL to proxy requests through\n+   *   * **agent** [http.Agent, https.Agent] &mdash; the Agent object to perform\n+   *     HTTP requests with. Used for connection pooling. Defaults to the global\n+   *     agent (`http.globalAgent`) for non-SSL connections. Note that for\n+   *     SSL connections, a special Agent object is used in order to enable\n+   *     peer certificate verification. This feature is only available in the\n+   *     Node.js environment.\n+   *   * **connectTimeout** [Integer] &mdash; Sets the socket to timeout after\n+   *     failing to establish a connection with the server after\n+   *     `connectTimeout` milliseconds. This timeout has no effect once a socket\n+   *     connection has been established.\n+   *   * **timeout** [Integer] &mdash; Sets the socket to timeout after timeout\n+   *     milliseconds of inactivity on the socket. Defaults to two minutes\n+   *     (120000).\n+   *   * **xhrAsync** [Boolean] &mdash; Whether the SDK will send asynchronous\n+   *     HTTP requests. Used in the browser environment only. Set to false to\n+   *     send requests synchronously. Defaults to true (async on).\n+   *   * **xhrWithCredentials** [Boolean] &mdash; Sets the \"withCredentials\"\n+   *     property of an XMLHttpRequest object. Used in the browser environment\n+   *     only. Defaults to false.\n+   */\n+  constructor: function ProcessCredentials(options) {\n+    AWS.Credentials.call(this);\n+\n+    options = options || {};\n+\n+    this.filename = options.filename;\n+    this.profile = options.profile || process.env.AWS_PROFILE || AWS.util.defaultProfile;\n+    this.httpOptions = options.httpOptions || null;\n+    this.get(options.callback || AWS.util.fn.noop);\n+  },\n+\n+  /**\n+   * @api private\n+   */\n+  load: function load(callback) {\n+    var self = this;\n+    try {\n+      var profiles = {};\n+      var profilesFromConfig = {};\n+      if (process.env[AWS.util.configOptInEnv]) {\n+        var profilesFromConfig = iniLoader.loadFrom({\n+          isConfig: true,\n+          filename: process.env[AWS.util.sharedConfigFileEnv]\n+        });\n+      }\n+      var profilesFromCreds = iniLoader.loadFrom({\n+        filename: this.filename ||\n+          (process.env[AWS.util.configOptInEnv] && process.env[AWS.util.sharedCredentialsFileEnv])\n+      });\n+      for (var i = 0, profileNames = Object.keys(profilesFromCreds); i < profileNames.length; i++) {\n+        profiles[profileNames[i]] = profilesFromCreds[profileNames[i]];\n+      }\n+      // load after profilesFromCreds to prefer profilesFromConfig\n+      for (var i = 0, profileNames = Object.keys(profilesFromConfig); i < profileNames.length; i++) {\n+        profiles[profileNames[i]] = profilesFromConfig[profileNames[i]];\n+      }\n+      var profile = profiles[this.profile] || {};\n+\n+      if (Object.keys(profile).length === 0) {\n+        throw AWS.util.error(\n+          new Error('Profile ' + this.profile + ' not found'),\n+          { code: 'ProcessCredentialsProviderFailure' }\n+        );\n+      }\n+\n+      if (profile['credential_process']) {\n+        this.loadViaCredentialProcess(profile, function(err, data) {\n+          if (err) {\n+            callback(err, null);\n+          } else {\n+            self.expired = false;\n+            self.accessKeyId = data.AccessKeyId;\n+            self.secretAccessKey = data.SecretAccessKey;\n+            self.sessionToken = data.SessionToken;\n+            if (data.Expiration) {\n+              self.expireTime = new Date(data.Expiration);\n+            }\n+            callback(null);\n+          }\n+        });\n+      } else {\n+        throw AWS.util.error(\n+          new Error('Profile ' + this.profile + ' did not include credential process'),\n+          { code: 'ProcessCredentialsProviderFailure' }\n+        );\n+      }\n+      this.expired = false;\n+      if (this.accessKeyId && this.secretAccessKey) {\n+        callback(null);\n+      }\n+    } catch (err) {\n+      callback(err);\n+    }\n+  },\n+\n+  /**\n+  * Executes the credential_process and retrieves\n+  * credentials from the output\n+  * @api private\n+  * @param profile [map] credentials profile\n+  * @throws SharedIniFileCredentialsProviderFailure\n+  */\n+  loadViaCredentialProcess: function loadViaCredentialProcess(profile, callback) {\n+    proc.exec(profile['credential_process'], function(err,stdOut, stdErr) {\n+      try {\n+        var credData = JSON.parse(stdOut);\n+        if (credData.Expiration) {\n+          var currentTime = AWS.util.date.getDate();\n+          var expireTime = new Date(credData.Expiration);\n+          if (expireTime < currentTime) {\n+            err = AWS.util.error(\n+              new Error('credential_process returned expired credentials'),\n+              { code: 'ProcessCredentialsProviderFailure' }\n+            );\n+          }\n+        } else if (credData.Version !== 1) {\n+          err = AWS.util.error(\n+            new Error('credential_process does not return Version == 1'),\n+          { code: 'ProcessCredentialsProviderFailure' }\n+          );\n+        }\n+        if (err) {",
        "comment_created_at": "2019-03-22T14:56:10+00:00",
        "comment_author": "jstewmon",
        "comment_body": "I think `err` should be checked before trying to process `stdOut`, since the condition is always checked.",
        "pr_file_module": null
      }
    ]
  }
]
