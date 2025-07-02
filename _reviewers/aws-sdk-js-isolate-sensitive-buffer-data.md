---
title: Isolate sensitive buffer data
description: When handling sensitive data in Node.js, protect against data leakage
  by isolating sensitive content in dedicated buffers. Node.js can create Buffers
  that aren't fully isolated, where `buf.byteLength !== buf.buffer.byteLength`, meaning
  sensitive data might be accessible to other code through the shared buffer memory.
repository: aws/aws-sdk-js
label: Security
language: Javascript
comments_count: 1
repository_stars: 7628
---

When handling sensitive data in Node.js, protect against data leakage by isolating sensitive content in dedicated buffers. Node.js can create Buffers that aren't fully isolated, where `buf.byteLength !== buf.buffer.byteLength`, meaning sensitive data might be accessible to other code through the shared buffer memory.

For sensitive operations like decoding credentials or encryption keys:

```javascript
// Secure approach for handling sensitive binary data
function handleSensitiveData(base64Value) {
  // Decode the base64 data
  const buf = util.base64.decode(value);
  
  // For sensitive data, ensure isolation in Node.js
  if (this.isSensitive && util.isNode() && typeof util.Buffer.alloc === 'function') {
    /* Node.js can create a Buffer that is not isolated.
     * i.e. buf.byteLength !== buf.buffer.byteLength
     * This means that sensitive data is accessible to anyone with access to buf.buffer.
     * If this is the node shared Buffer, then other code within this process _could_ find this secret.
     * Copy sensitive data to an isolated Buffer and zero the sensitive data.
     */
    const copy = util.Buffer.alloc(buf.length);
    buf.copy(copy);
    buf.fill(0); // Zero the original buffer
    return copy;
  }
  
  return buf;
}
```

Always consider whether your data is sensitive and might require this additional protection. This pattern is particularly important when handling authentication tokens, encryption keys, and other credentials.


[
  {
    "discussion_id": "274981081",
    "pr_number": 2622,
    "pr_file": "lib/model/shape.js",
    "created_at": "2019-04-12T16:35:33+00:00",
    "commented_code": "function BinaryShape() {\n  Shape.apply(this, arguments);\n  this.toType = util.base64.decode;\n  this.toType = function(value) {\n    var buf = util.base64.decode(value);\n    if (this.isSensitive && util.isNode() && typeof util.Buffer.alloc === 'function') {",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "274981081",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 2622,
        "pr_file": "lib/model/shape.js",
        "discussion_id": "274981081",
        "commented_code": "@@ -354,7 +354,16 @@ function IntegerShape() {\n \n function BinaryShape() {\n   Shape.apply(this, arguments);\n-  this.toType = util.base64.decode;\n+  this.toType = function(value) {\n+    var buf = util.base64.decode(value);\n+    if (this.isSensitive && util.isNode() && typeof util.Buffer.alloc === 'function') {",
        "comment_created_at": "2019-04-12T16:35:33+00:00",
        "comment_author": "seebees",
        "comment_body": "Maybe a comment to explain why.  Word smith to your liking :)\r\n\r\n```javascript\r\n  /* Node.js can create a Buffer that is not isolated.\r\n   * i.e. buf.byteLength !== buf.buffer.byteLength\r\n   * This means that the sensitive data is accessible to anyone with access to buf.buffer.\r\n   * If this is the node shared Buffer, then other code within this process _could_ find this secret.\r\n   * Copy sensitive data to an isolated Buffer and zero the sensitive data.\r\n   * While this is safe to do here, copying this code somewhere else may produce unexpected results.\r\n   */\r\n```\r\n\r\nAdditionally, why not check `buf.byteLength !== buf.buffer.byteLength`?  And then handle the solution in node or the browser?",
        "pr_file_module": null
      },
      {
        "comment_id": "275458536",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 2622,
        "pr_file": "lib/model/shape.js",
        "discussion_id": "274981081",
        "commented_code": "@@ -354,7 +354,16 @@ function IntegerShape() {\n \n function BinaryShape() {\n   Shape.apply(this, arguments);\n-  this.toType = util.base64.decode;\n+  this.toType = function(value) {\n+    var buf = util.base64.decode(value);\n+    if (this.isSensitive && util.isNode() && typeof util.Buffer.alloc === 'function') {",
        "comment_created_at": "2019-04-15T17:08:02+00:00",
        "comment_author": "AllanZhengYP",
        "comment_body": "Thanks for the information, I will update the comment. \r\n> why not check buf.byteLength !== buf.buffer.byteLength?\r\n\r\nI'm not sure whether `buf.buffer` would be undefined in browser polyfill, it's just safer this way. And it's not clear in Node doc on when the `buf.buffer` is added. In very old Node, it should be `buf.parent`. Checking availability of `alloc` seems clearer and safer because we will use this API to locate the buffer anyway.",
        "pr_file_module": null
      }
    ]
  }
]
