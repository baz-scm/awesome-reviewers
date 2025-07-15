---
title: Handle streams properly
description: When transferring data over HTTP, properly implement streaming mechanisms
  to prevent memory exhaustion and potential denial-of-service vulnerabilities. Handle
  backpressure appropriately to ensure that slow clients cannot overwhelm server resources.
repository: expressjs/express
label: Networking
language: JavaScript
comments_count: 5
repository_stars: 67300
---

When transferring data over HTTP, properly implement streaming mechanisms to prevent memory exhaustion and potential denial-of-service vulnerabilities. Handle backpressure appropriately to ensure that slow clients cannot overwhelm server resources.

Key considerations:
1. For large data transfers, use appropriate streaming APIs instead of loading entire payloads into memory
2. Always handle backpressure in custom stream implementations
3. Be aware of client disconnections and abort events to free resources promptly
4. Choose the right stream API based on data source and Node.js version compatibility
5. Ensure HTTP header consistency with your streaming approach (avoid setting Content-Length with Transfer-Encoding)

Example of properly handling a Blob response with backpressure consideration:

```javascript
// Good: Using stream.Readable.from with proper error handling
if (isChunkBlob) {
  var res = this;
  var blob = chunk;
  
  if (typeof blob.stream === 'function') {
    var Readable = require('stream').Readable;
    var nodeStream = Readable.from(blob.stream());
    
    // Handle errors and cleanup on request termination
    nodeStream.on('error', req.next);
    res.on('error', req.next);
    
    // Use pipe to automatically handle backpressure
    nodeStream.pipe(res);
  } else {
    // Fallback for blobs without stream support
    blob.arrayBuffer()
      .then(function(arrayBuffer) {
        res.end(Buffer.from(arrayBuffer));
      })
      .catch(req.next);
  }
} else {
  this.end(chunk, encoding);
}
```

For custom streaming implementations, always account for backpressure by responding to write events that return false, and implement proper error handling to release resources when connections terminate unexpectedly.