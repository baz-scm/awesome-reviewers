---
title: Structured test resource management
description: Organize tests with proper resource lifecycle management to ensure reliability
  and maintainability. Create test resources once in `before` hooks rather than in
  individual tests, and clean them up in corresponding `after` hooks. For shared resources,
  use unique identifiers (e.g., timestamps) to prevent conflicts between test runs.
repository: aws/aws-sdk-js
label: Testing
language: JavaScript
comments_count: 5
repository_stars: 7628
---

Organize tests with proper resource lifecycle management to ensure reliability and maintainability. Create test resources once in `before` hooks rather than in individual tests, and clean them up in corresponding `after` hooks. For shared resources, use unique identifiers (e.g., timestamps) to prevent conflicts between test runs.

Group related tests into logical suites using descriptive `describe` blocks to improve organization and simplify cleanup:

```javascript
describe('S3 object operations', function() {
  var s3;
  var bucketName = 'test-bucket-' + Date.now(); // Unique identifier

  before(function(done) {
    s3 = new AWS.S3();
    // Create resources once
    s3.createBucket({Bucket: bucketName}).promise()
      .then(function() {
        return s3.waitFor('bucketExists', {Bucket: bucketName}).promise();
      })
      .then(function() {
        done();
      });
  });

  after(function(done) {
    // Clean up resources in corresponding after hook
    s3.deleteBucket({Bucket: bucketName}).promise()
      .then(function() {
        done();
      });
  });

  // Individual tests that use the shared bucket
  it('should upload an object', function() {
    // Test implementation
  });

  it('should download an object', function() {
    // Test implementation
  });
});
```

This approach prevents resource exhaustion, improves test execution speed, and reduces flakiness from race conditions or rate limiting. Separating environment-specific tests (browser vs. Node.js) into different folders further improves organization and prevents execution in incorrect environments.
