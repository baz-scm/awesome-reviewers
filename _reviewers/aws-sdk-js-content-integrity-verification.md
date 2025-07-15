---
title: Content integrity verification
description: 'When handling HTTP responses, especially with streaming data, properly
  verify content integrity and length to prevent data corruption or unexpected termination.
  Key considerations:'
repository: aws/aws-sdk-js
label: Networking
language: JavaScript
comments_count: 5
repository_stars: 7628
---

When handling HTTP responses, especially with streaming data, properly verify content integrity and length to prevent data corruption or unexpected termination. Key considerations:

1. **Content-Length may not match actual data size** when responses use compression (gzip, br, deflate). In such cases:
   - Check for Content-Encoding header to determine if response is compressed
   - Use actual byte counts rather than Content-Length for progress tracking
   - Consider sending Accept-Encoding: identity for critical operations requiring precise progress tracking

2. **Implement proper stream handling** based on environment:
   - For Node.js, use Transform streams rather than 'data' event listeners to avoid backpressure issues:
   ```javascript
   // GOOD: Use piping with Transform streams
   var contentLengthCheckerStream = new ContentLengthCheckerStream(
     parseInt(headers['content-length'], 10)
   );
   responseStream.pipe(contentLengthCheckerStream).pipe(stream);
   
   // AVOID: Direct data event listeners can cause backpressure issues in older Node.js
   responseStream.on('data', function(chunk) {
     receivedLen += chunk.length;
     // potential for data loss in Node.js <= 0.10.x
   });
   ```

3. **Handle content integrity verification** for both Node.js and browser environments:
   - In Node.js, implement pipe-through verification streams
   - In browsers, buffer response data for integrity checks
   - Verify checksums/hashes when provided in response headers
   - Emit appropriate errors with descriptive messages when content length or integrity checks fail

Implementing these practices ensures data is received completely and correctly, preventing subtle bugs in network communication.
