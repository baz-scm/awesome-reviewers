---
title: Structured test resource management
description: Organize tests with proper resource lifecycle management to ensure reliability
  and maintainability. Create test resources once in `before` hooks rather than in
  individual tests, and clean them up in corresponding `after` hooks. For shared resources,
  use unique identifiers (e.g., timestamps) to prevent conflicts between test runs.
repository: aws/aws-sdk-js
label: Testing
language: Javascript
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


[
  {
    "discussion_id": "182547608",
    "pr_number": 2014,
    "pr_file": "test/browserHashes.spec.js",
    "created_at": "2018-04-18T19:46:02+00:00",
    "commented_code": "if (truncate) {\n                            digest = digest.slice(0, truncate);\n                        }\n                        expect(digest.toString('hex')).to.equal(expected);\n                        //in node <= 0.10 digest sometimes returns a Dataview, should be buffer.",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "182547608",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 2014,
        "pr_file": "test/browserHashes.spec.js",
        "discussion_id": "182547608",
        "commented_code": "@@ -43,7 +43,11 @@ describe('Browser hash implementations', function() {\n                         if (truncate) {\n                             digest = digest.slice(0, truncate);\n                         }\n-                        expect(digest.toString('hex')).to.equal(expected);\n+                        //in node <= 0.10 digest sometimes returns a Dataview, should be buffer.",
        "comment_created_at": "2018-04-18T19:46:02+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Are these tests running in node.js? This should only be running in browser environments, and is using the 3rd party `Buffer` package instead of node.js' `Buffer` package. We can place browser-specific tests in a separate folder and exclude them from being run by mocha in the npm unit script.",
        "pr_file_module": null
      },
      {
        "comment_id": "182572206",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 2014,
        "pr_file": "test/browserHashes.spec.js",
        "discussion_id": "182547608",
        "commented_code": "@@ -43,7 +43,11 @@ describe('Browser hash implementations', function() {\n                         if (truncate) {\n                             digest = digest.slice(0, truncate);\n                         }\n-                        expect(digest.toString('hex')).to.equal(expected);\n+                        //in node <= 0.10 digest sometimes returns a Dataview, should be buffer.",
        "comment_created_at": "2018-04-18T21:16:49+00:00",
        "comment_author": "AllanZhengYP",
        "comment_body": "Ah right! The change mean to fix the test. But actually we can remove it out of node test. I didn't realize this is browser-only although the name already told me",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "184547814",
    "pr_number": 1956,
    "pr_file": "test/integration_test/helpers.js",
    "created_at": "2018-04-26T22:22:30+00:00",
    "commented_code": "(function() {\n  global.expect = require('chai').expect;\n  module.exports = {\n    sharedBucket: 'aws-sdk-js-integration',",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "184547814",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1956,
        "pr_file": "test/integration_test/helpers.js",
        "discussion_id": "184547814",
        "commented_code": "@@ -0,0 +1,25 @@\n+(function() {\n+  global.expect = require('chai').expect;\n+  module.exports = {\n+    sharedBucket: 'aws-sdk-js-integration',",
        "comment_created_at": "2018-04-26T22:22:30+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Probably want to append a timestamp to this as well to make it somewhat unique",
        "pr_file_module": null
      },
      {
        "comment_id": "184557074",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1956,
        "pr_file": "test/integration_test/helpers.js",
        "discussion_id": "184547814",
        "commented_code": "@@ -0,0 +1,25 @@\n+(function() {\n+  global.expect = require('chai').expect;\n+  module.exports = {\n+    sharedBucket: 'aws-sdk-js-integration',",
        "comment_created_at": "2018-04-26T23:19:53+00:00",
        "comment_author": "AllanZhengYP",
        "comment_body": "This is for sharing the test bucket. Maybe this time occasionally we fail to delete the bucket. But next time we will delete this bucket.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "184550574",
    "pr_number": 1956,
    "pr_file": "test/integration_test/s3/getObject.spec.js",
    "created_at": "2018-04-26T22:38:16+00:00",
    "commented_code": "var helpers = require('../helpers');\nvar AWS = helpers.AWS;\nvar bucketName = helpers.sharedBucket;\ndescribe('download integrity', function() {\n  var params;\n  var s3;\n  function putObject(customParams, done) {\n    params = {\n      Bucket: customParams.Bucket || params.Bucket,\n      Key: customParams.Key || params.Key,\n    };\n    s3.createBucket({Bucket: params.Bucket}).promise().then(function() {\n      return s3.waitFor('bucketExists', {Bucket: params.Bucket}).promise()\n    }).then(function() {\n      return s3.putObject({\n        Bucket: params.Bucket,\n        Key: params.Key,\n        Body: customParams.Body || params.Body\n      }).promise();\n    }).then(function() {\n      return s3.waitFor('objectExists', {\n        Bucket: params.Bucket,\n        Key: params.Key,\n      }).promise();\n    }).then(function() { \n      if (typeof done === 'function') done();\n    }).catch(function(err) {\n      throw new Error('Cannot put object: ' + err);\n      exit(1);\n    });\n  }\n\n  function delectBucket(done) {\n    s3.listObjectVersions({\n      Bucket: params.Bucket\n    }).promise().then(function(data) {\n      var removeObjectsParams = {\n        Bucket: params.Bucket,\n        Delete: {\n          Quiet: false,\n          Objects: []\n        }\n      }\n      for (var version of data.Versions) {\n        removeObjectsParams.Delete.Objects.push({\n          Key: version.Key,\n          VersionId: version.VersionId === 'null' ? null : version.VersionId,\n        });\n      }\n      return removeObjectsParams;\n    }).then(function(removeObjectsParams) {\n      return s3.deleteObjects(removeObjectsParams).promise();\n    }).then(function() {\n      return s3.waitFor('objectNotExists', {\n        Bucket: params.Bucket,\n        Key: params.Key,\n      }).promise()\n    }).then(function() {\n      return s3.deleteBucket({Bucket: params.Bucket}).promise();\n    }).then(function(data) {\n      return s3.waitFor('bucketNotExists', {Bucket: params.Bucket}).promise();\n    }).then(function() {\n      if (typeof done === 'function') done();\n    }).catch(function(err) {\n      throw new Error('Cannot delete bucket: ' + err);\n      exit(1);\n    })\n  }\n\n  before('setup s3 client with responseChecksumAlgorithm equals \\'md5\\'', function() {\n    s3 = new AWS.S3({responseChecksumAlgorithm: 'md5'});",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "184550574",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1956,
        "pr_file": "test/integration_test/s3/getObject.spec.js",
        "discussion_id": "184550574",
        "commented_code": "@@ -0,0 +1,209 @@\n+var helpers = require('../helpers');\n+var AWS = helpers.AWS;\n+var bucketName = helpers.sharedBucket;\n+describe('download integrity', function() {\n+  var params;\n+  var s3;\n+  function putObject(customParams, done) {\n+    params = {\n+      Bucket: customParams.Bucket || params.Bucket,\n+      Key: customParams.Key || params.Key,\n+    };\n+    s3.createBucket({Bucket: params.Bucket}).promise().then(function() {\n+      return s3.waitFor('bucketExists', {Bucket: params.Bucket}).promise()\n+    }).then(function() {\n+      return s3.putObject({\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+        Body: customParams.Body || params.Body\n+      }).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise();\n+    }).then(function() { \n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot put object: ' + err);\n+      exit(1);\n+    });\n+  }\n+\n+  function delectBucket(done) {\n+    s3.listObjectVersions({\n+      Bucket: params.Bucket\n+    }).promise().then(function(data) {\n+      var removeObjectsParams = {\n+        Bucket: params.Bucket,\n+        Delete: {\n+          Quiet: false,\n+          Objects: []\n+        }\n+      }\n+      for (var version of data.Versions) {\n+        removeObjectsParams.Delete.Objects.push({\n+          Key: version.Key,\n+          VersionId: version.VersionId === 'null' ? null : version.VersionId,\n+        });\n+      }\n+      return removeObjectsParams;\n+    }).then(function(removeObjectsParams) {\n+      return s3.deleteObjects(removeObjectsParams).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectNotExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise()\n+    }).then(function() {\n+      return s3.deleteBucket({Bucket: params.Bucket}).promise();\n+    }).then(function(data) {\n+      return s3.waitFor('bucketNotExists', {Bucket: params.Bucket}).promise();\n+    }).then(function() {\n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot delete bucket: ' + err);\n+      exit(1);\n+    })\n+  }\n+\n+  before('setup s3 client with responseChecksumAlgorithm equals \\'md5\\'', function() {\n+    s3 = new AWS.S3({responseChecksumAlgorithm: 'md5'});",
        "comment_created_at": "2018-04-26T22:38:16+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Why don't you create the bucket used by all the tests in the `before` step? We shouldn't have to create a new bucket for every single test, just this suite of tests. \r\n\r\nI also wouldn't mix the `putObject` method with `createBucket`. `putObject` is doing too much, and adds 'global' (across tests) state. For example, you don't directly pass it the bucket or key, instead relying on a closure that every test has access to (and can change). That could lead to tricky edge cases coming up later that are hard to debug.",
        "pr_file_module": null
      },
      {
        "comment_id": "184559113",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1956,
        "pr_file": "test/integration_test/s3/getObject.spec.js",
        "discussion_id": "184550574",
        "commented_code": "@@ -0,0 +1,209 @@\n+var helpers = require('../helpers');\n+var AWS = helpers.AWS;\n+var bucketName = helpers.sharedBucket;\n+describe('download integrity', function() {\n+  var params;\n+  var s3;\n+  function putObject(customParams, done) {\n+    params = {\n+      Bucket: customParams.Bucket || params.Bucket,\n+      Key: customParams.Key || params.Key,\n+    };\n+    s3.createBucket({Bucket: params.Bucket}).promise().then(function() {\n+      return s3.waitFor('bucketExists', {Bucket: params.Bucket}).promise()\n+    }).then(function() {\n+      return s3.putObject({\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+        Body: customParams.Body || params.Body\n+      }).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise();\n+    }).then(function() { \n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot put object: ' + err);\n+      exit(1);\n+    });\n+  }\n+\n+  function delectBucket(done) {\n+    s3.listObjectVersions({\n+      Bucket: params.Bucket\n+    }).promise().then(function(data) {\n+      var removeObjectsParams = {\n+        Bucket: params.Bucket,\n+        Delete: {\n+          Quiet: false,\n+          Objects: []\n+        }\n+      }\n+      for (var version of data.Versions) {\n+        removeObjectsParams.Delete.Objects.push({\n+          Key: version.Key,\n+          VersionId: version.VersionId === 'null' ? null : version.VersionId,\n+        });\n+      }\n+      return removeObjectsParams;\n+    }).then(function(removeObjectsParams) {\n+      return s3.deleteObjects(removeObjectsParams).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectNotExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise()\n+    }).then(function() {\n+      return s3.deleteBucket({Bucket: params.Bucket}).promise();\n+    }).then(function(data) {\n+      return s3.waitFor('bucketNotExists', {Bucket: params.Bucket}).promise();\n+    }).then(function() {\n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot delete bucket: ' + err);\n+      exit(1);\n+    })\n+  }\n+\n+  before('setup s3 client with responseChecksumAlgorithm equals \\'md5\\'', function() {\n+    s3 = new AWS.S3({responseChecksumAlgorithm: 'md5'});",
        "comment_created_at": "2018-04-26T23:33:37+00:00",
        "comment_author": "AllanZhengYP",
        "comment_body": "Yes, you can pass in the bucket and key, but right, it will change the global state. But capsulizing them will also guarantee `putObject` always succeed(bucket always there).",
        "pr_file_module": null
      },
      {
        "comment_id": "184560586",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1956,
        "pr_file": "test/integration_test/s3/getObject.spec.js",
        "discussion_id": "184550574",
        "commented_code": "@@ -0,0 +1,209 @@\n+var helpers = require('../helpers');\n+var AWS = helpers.AWS;\n+var bucketName = helpers.sharedBucket;\n+describe('download integrity', function() {\n+  var params;\n+  var s3;\n+  function putObject(customParams, done) {\n+    params = {\n+      Bucket: customParams.Bucket || params.Bucket,\n+      Key: customParams.Key || params.Key,\n+    };\n+    s3.createBucket({Bucket: params.Bucket}).promise().then(function() {\n+      return s3.waitFor('bucketExists', {Bucket: params.Bucket}).promise()\n+    }).then(function() {\n+      return s3.putObject({\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+        Body: customParams.Body || params.Body\n+      }).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise();\n+    }).then(function() { \n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot put object: ' + err);\n+      exit(1);\n+    });\n+  }\n+\n+  function delectBucket(done) {\n+    s3.listObjectVersions({\n+      Bucket: params.Bucket\n+    }).promise().then(function(data) {\n+      var removeObjectsParams = {\n+        Bucket: params.Bucket,\n+        Delete: {\n+          Quiet: false,\n+          Objects: []\n+        }\n+      }\n+      for (var version of data.Versions) {\n+        removeObjectsParams.Delete.Objects.push({\n+          Key: version.Key,\n+          VersionId: version.VersionId === 'null' ? null : version.VersionId,\n+        });\n+      }\n+      return removeObjectsParams;\n+    }).then(function(removeObjectsParams) {\n+      return s3.deleteObjects(removeObjectsParams).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectNotExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise()\n+    }).then(function() {\n+      return s3.deleteBucket({Bucket: params.Bucket}).promise();\n+    }).then(function(data) {\n+      return s3.waitFor('bucketNotExists', {Bucket: params.Bucket}).promise();\n+    }).then(function() {\n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot delete bucket: ' + err);\n+      exit(1);\n+    })\n+  }\n+\n+  before('setup s3 client with responseChecksumAlgorithm equals \\'md5\\'', function() {\n+    s3 = new AWS.S3({responseChecksumAlgorithm: 'md5'});",
        "comment_created_at": "2018-04-26T23:44:33+00:00",
        "comment_author": "chrisradek",
        "comment_body": "But you could also make sure the bucket is there in the `before` hook. Just call `done()` after the `waitFor` method completes. Then you also only need to create it once; I don't think there's a reason we need to create a new bucket for every test since we aren't testing any bucket-specific configurations here. Creating a new bucket with each test also creates more points of failure (rate/resource limits, for example).\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "184561348",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1956,
        "pr_file": "test/integration_test/s3/getObject.spec.js",
        "discussion_id": "184550574",
        "commented_code": "@@ -0,0 +1,209 @@\n+var helpers = require('../helpers');\n+var AWS = helpers.AWS;\n+var bucketName = helpers.sharedBucket;\n+describe('download integrity', function() {\n+  var params;\n+  var s3;\n+  function putObject(customParams, done) {\n+    params = {\n+      Bucket: customParams.Bucket || params.Bucket,\n+      Key: customParams.Key || params.Key,\n+    };\n+    s3.createBucket({Bucket: params.Bucket}).promise().then(function() {\n+      return s3.waitFor('bucketExists', {Bucket: params.Bucket}).promise()\n+    }).then(function() {\n+      return s3.putObject({\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+        Body: customParams.Body || params.Body\n+      }).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise();\n+    }).then(function() { \n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot put object: ' + err);\n+      exit(1);\n+    });\n+  }\n+\n+  function delectBucket(done) {\n+    s3.listObjectVersions({\n+      Bucket: params.Bucket\n+    }).promise().then(function(data) {\n+      var removeObjectsParams = {\n+        Bucket: params.Bucket,\n+        Delete: {\n+          Quiet: false,\n+          Objects: []\n+        }\n+      }\n+      for (var version of data.Versions) {\n+        removeObjectsParams.Delete.Objects.push({\n+          Key: version.Key,\n+          VersionId: version.VersionId === 'null' ? null : version.VersionId,\n+        });\n+      }\n+      return removeObjectsParams;\n+    }).then(function(removeObjectsParams) {\n+      return s3.deleteObjects(removeObjectsParams).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectNotExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise()\n+    }).then(function() {\n+      return s3.deleteBucket({Bucket: params.Bucket}).promise();\n+    }).then(function(data) {\n+      return s3.waitFor('bucketNotExists', {Bucket: params.Bucket}).promise();\n+    }).then(function() {\n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot delete bucket: ' + err);\n+      exit(1);\n+    })\n+  }\n+\n+  before('setup s3 client with responseChecksumAlgorithm equals \\'md5\\'', function() {\n+    s3 = new AWS.S3({responseChecksumAlgorithm: 'md5'});",
        "comment_created_at": "2018-04-26T23:50:42+00:00",
        "comment_author": "AllanZhengYP",
        "comment_body": "yea. I will move the `putObject` to `before` trait. And use timestamp in bucket name. I was thinking that we can write less code if we are going to add more tests here. But now I agree that this is an overkill and not worthwhile. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "184550641",
    "pr_number": 1956,
    "pr_file": "test/integration_test/s3/getObject.spec.js",
    "created_at": "2018-04-26T22:38:41+00:00",
    "commented_code": "var helpers = require('../helpers');\nvar AWS = helpers.AWS;\nvar bucketName = helpers.sharedBucket;\ndescribe('download integrity', function() {\n  var params;\n  var s3;\n  function putObject(customParams, done) {\n    params = {\n      Bucket: customParams.Bucket || params.Bucket,\n      Key: customParams.Key || params.Key,\n    };\n    s3.createBucket({Bucket: params.Bucket}).promise().then(function() {\n      return s3.waitFor('bucketExists', {Bucket: params.Bucket}).promise()\n    }).then(function() {\n      return s3.putObject({\n        Bucket: params.Bucket,\n        Key: params.Key,\n        Body: customParams.Body || params.Body\n      }).promise();\n    }).then(function() {\n      return s3.waitFor('objectExists', {\n        Bucket: params.Bucket,\n        Key: params.Key,\n      }).promise();\n    }).then(function() { \n      if (typeof done === 'function') done();\n    }).catch(function(err) {\n      throw new Error('Cannot put object: ' + err);\n      exit(1);\n    });\n  }\n\n  function delectBucket(done) {\n    s3.listObjectVersions({\n      Bucket: params.Bucket\n    }).promise().then(function(data) {\n      var removeObjectsParams = {\n        Bucket: params.Bucket,\n        Delete: {\n          Quiet: false,\n          Objects: []\n        }\n      }\n      for (var version of data.Versions) {\n        removeObjectsParams.Delete.Objects.push({\n          Key: version.Key,\n          VersionId: version.VersionId === 'null' ? null : version.VersionId,\n        });\n      }\n      return removeObjectsParams;\n    }).then(function(removeObjectsParams) {\n      return s3.deleteObjects(removeObjectsParams).promise();\n    }).then(function() {\n      return s3.waitFor('objectNotExists', {\n        Bucket: params.Bucket,\n        Key: params.Key,\n      }).promise()\n    }).then(function() {\n      return s3.deleteBucket({Bucket: params.Bucket}).promise();\n    }).then(function(data) {\n      return s3.waitFor('bucketNotExists', {Bucket: params.Bucket}).promise();\n    }).then(function() {\n      if (typeof done === 'function') done();\n    }).catch(function(err) {\n      throw new Error('Cannot delete bucket: ' + err);\n      exit(1);\n    })\n  }\n\n  before('setup s3 client with responseChecksumAlgorithm equals \\'md5\\'', function() {\n    s3 = new AWS.S3({responseChecksumAlgorithm: 'md5'});\n  })\n\n  beforeEach('setup bucket and object...', function(done) {\n    params = {\n      Bucket: bucketName,\n      Key: 'key',\n    };\n    putObject({Body: 'this is a test!'}, done);\n  })\n\n  afterEach('delete bucket...', function(done) {",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "184550641",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1956,
        "pr_file": "test/integration_test/s3/getObject.spec.js",
        "discussion_id": "184550641",
        "commented_code": "@@ -0,0 +1,209 @@\n+var helpers = require('../helpers');\n+var AWS = helpers.AWS;\n+var bucketName = helpers.sharedBucket;\n+describe('download integrity', function() {\n+  var params;\n+  var s3;\n+  function putObject(customParams, done) {\n+    params = {\n+      Bucket: customParams.Bucket || params.Bucket,\n+      Key: customParams.Key || params.Key,\n+    };\n+    s3.createBucket({Bucket: params.Bucket}).promise().then(function() {\n+      return s3.waitFor('bucketExists', {Bucket: params.Bucket}).promise()\n+    }).then(function() {\n+      return s3.putObject({\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+        Body: customParams.Body || params.Body\n+      }).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise();\n+    }).then(function() { \n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot put object: ' + err);\n+      exit(1);\n+    });\n+  }\n+\n+  function delectBucket(done) {\n+    s3.listObjectVersions({\n+      Bucket: params.Bucket\n+    }).promise().then(function(data) {\n+      var removeObjectsParams = {\n+        Bucket: params.Bucket,\n+        Delete: {\n+          Quiet: false,\n+          Objects: []\n+        }\n+      }\n+      for (var version of data.Versions) {\n+        removeObjectsParams.Delete.Objects.push({\n+          Key: version.Key,\n+          VersionId: version.VersionId === 'null' ? null : version.VersionId,\n+        });\n+      }\n+      return removeObjectsParams;\n+    }).then(function(removeObjectsParams) {\n+      return s3.deleteObjects(removeObjectsParams).promise();\n+    }).then(function() {\n+      return s3.waitFor('objectNotExists', {\n+        Bucket: params.Bucket,\n+        Key: params.Key,\n+      }).promise()\n+    }).then(function() {\n+      return s3.deleteBucket({Bucket: params.Bucket}).promise();\n+    }).then(function(data) {\n+      return s3.waitFor('bucketNotExists', {Bucket: params.Bucket}).promise();\n+    }).then(function() {\n+      if (typeof done === 'function') done();\n+    }).catch(function(err) {\n+      throw new Error('Cannot delete bucket: ' + err);\n+      exit(1);\n+    })\n+  }\n+\n+  before('setup s3 client with responseChecksumAlgorithm equals \\'md5\\'', function() {\n+    s3 = new AWS.S3({responseChecksumAlgorithm: 'md5'});\n+  })\n+\n+  beforeEach('setup bucket and object...', function(done) {\n+    params = {\n+      Bucket: bucketName,\n+      Key: 'key',\n+    };\n+    putObject({Body: 'this is a test!'}, done);\n+  })\n+\n+  afterEach('delete bucket...', function(done) {",
        "comment_created_at": "2018-04-26T22:38:41+00:00",
        "comment_author": "chrisradek",
        "comment_body": "If you `createBucket` in the `before` hook, you can `deleteBucket` in the `after` hook!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "265341875",
    "pr_number": 2559,
    "pr_file": "test/credentials.spec.js",
    "created_at": "2019-03-13T21:37:20+00:00",
    "commented_code": "creds.get();\n          return validateCredentials(creds);\n        });\n        it('loads via credential_process', function(done) {",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "265341875",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 2559,
        "pr_file": "test/credentials.spec.js",
        "discussion_id": "265341875",
        "commented_code": "@@ -438,6 +438,124 @@\n           creds.get();\n           return validateCredentials(creds);\n         });\n+        it('loads via credential_process', function(done) {",
        "comment_created_at": "2019-03-13T21:37:20+00:00",
        "comment_author": "AllanZhengYP",
        "comment_body": "Nit: you can put these unit tests to a test suite(like leading with `describe('credential process')`). So than you can clear the spies easily. ",
        "pr_file_module": null
      }
    ]
  }
]
