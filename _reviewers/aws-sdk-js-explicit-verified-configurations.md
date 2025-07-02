---
title: Explicit verified configurations
description: Always specify configuration values explicitly and verify their accuracy
  against official documentation or tests. This applies to region configurations,
  API settings, and credential management. Avoid mutations of global configuration
  objects, and instead set values explicitly when defined by service APIs.
repository: aws/aws-sdk-js
label: Configurations
language: Json
comments_count: 3
repository_stars: 7628
---

Always specify configuration values explicitly and verify their accuracy against official documentation or tests. This applies to region configurations, API settings, and credential management. Avoid mutations of global configuration objects, and instead set values explicitly when defined by service APIs.

Example:
```json
// GOOD: Explicitly verified region configuration
"us-iso-*/iam": {
  "endpoint": "{service}.us-iso-east-1.c2s.ic.gov",
  "globalEndpoint": true,
  "signingRegion": "us-iso-east-1"  // Verified against Endpoints 2.0 tests
}

// BAD: Incorrect or unverified configuration
"us-iso-*/iam": {
  "endpoint": "{service}.us-iso-east-1.c2s.ic.gov",
  "globalEndpoint": true,
  "signingRegion": "us-east-1"  // Incorrect region
}
```

For credential configurations, always use resolved credentials when available rather than relying on automatic refresh mechanisms that may cause performance issues.


[
  {
    "discussion_id": "1196576262",
    "pr_number": 4422,
    "pr_file": "lib/region_config_data.json",
    "created_at": "2023-05-17T14:03:21+00:00",
    "commented_code": "\"globalEndpoint\": true,\n      \"signingRegion\": \"cn-north-1\"\n    },\n    \"us-gov-*/iam\": \"globalGovCloud\",\n    \"us-iso-*/iam\": {\n      \"endpoint\": \"{service}.us-iso-east-1.c2s.ic.gov\",\n      \"globalEndpoint\": true,\n      \"signingRegion\": \"us-east-1\"",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "1196576262",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 4422,
        "pr_file": "lib/region_config_data.json",
        "discussion_id": "1196576262",
        "commented_code": "@@ -43,8 +43,13 @@\n       \"globalEndpoint\": true,\n       \"signingRegion\": \"cn-north-1\"\n     },\n-    \"us-gov-*/iam\": \"globalGovCloud\",\n+    \"us-iso-*/iam\": {\n+      \"endpoint\": \"{service}.us-iso-east-1.c2s.ic.gov\",\n+      \"globalEndpoint\": true,\n+      \"signingRegion\": \"us-east-1\"",
        "comment_created_at": "2023-05-17T14:03:21+00:00",
        "comment_author": "trivikr",
        "comment_body": "Should this be us-iso-east-1?\r\n```suggestion\r\n      \"signingRegion\": \"us-iso-east-1\"\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1196584529",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 4422,
        "pr_file": "lib/region_config_data.json",
        "discussion_id": "1196576262",
        "commented_code": "@@ -43,8 +43,13 @@\n       \"globalEndpoint\": true,\n       \"signingRegion\": \"cn-north-1\"\n     },\n-    \"us-gov-*/iam\": \"globalGovCloud\",\n+    \"us-iso-*/iam\": {\n+      \"endpoint\": \"{service}.us-iso-east-1.c2s.ic.gov\",\n+      \"globalEndpoint\": true,\n+      \"signingRegion\": \"us-east-1\"",
        "comment_created_at": "2023-05-17T14:09:18+00:00",
        "comment_author": "trivikr",
        "comment_body": "Verified that it should be `us-iso-east-1` from Endpoints 2.0 tests https://github.com/aws/aws-sdk-js-v3/blob/7ed7101dcc4e81038b6c7f581162b959e6b33a04/codegen/sdk-codegen/aws-models/iam.json#L2270-L2291",
        "pr_file_module": null
      },
      {
        "comment_id": "1198708906",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 4422,
        "pr_file": "lib/region_config_data.json",
        "discussion_id": "1196576262",
        "commented_code": "@@ -43,8 +43,13 @@\n       \"globalEndpoint\": true,\n       \"signingRegion\": \"cn-north-1\"\n     },\n-    \"us-gov-*/iam\": \"globalGovCloud\",\n+    \"us-iso-*/iam\": {\n+      \"endpoint\": \"{service}.us-iso-east-1.c2s.ic.gov\",\n+      \"globalEndpoint\": true,\n+      \"signingRegion\": \"us-east-1\"",
        "comment_created_at": "2023-05-19T08:46:01+00:00",
        "comment_author": "pinak",
        "comment_body": "Yes, thanks for catching that!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1034017482",
    "pr_number": 4288,
    "pr_file": ".changes/next-release/bugfix-region-config-31f590e0.json",
    "created_at": "2022-11-28T20:28:38+00:00",
    "commented_code": "{\n  \"type\": \"bugfix\",\n  \"category\": \"region_config\",\n  \"description\": \"avoid mutation in global object signatureVersion\"",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "1034017482",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 4288,
        "pr_file": ".changes/next-release/bugfix-region-config-31f590e0.json",
        "discussion_id": "1034017482",
        "commented_code": "@@ -0,0 +1,5 @@\n+{\n+  \"type\": \"bugfix\",\n+  \"category\": \"region_config\",\n+  \"description\": \"avoid mutation in global object signatureVersion\"",
        "comment_created_at": "2022-11-28T20:28:38+00:00",
        "comment_author": "trivikr",
        "comment_body": "```suggestion\r\n  \"description\": \"Set signatureVersion to bearer explcitly when defined in service API\"\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "608843822",
    "pr_number": 3700,
    "pr_file": ".changes/next-release/bugfix-ManagedUpload-2bd31158.json",
    "created_at": "2021-04-07T17:14:07+00:00",
    "commented_code": "{\n  \"type\": \"bugfix\",\n  \"category\": \"ManagedUpload\",\n  \"description\": \"fix a bug that credentials refresh to frequently\"",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "608843822",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 3700,
        "pr_file": ".changes/next-release/bugfix-ManagedUpload-2bd31158.json",
        "discussion_id": "608843822",
        "commented_code": "@@ -0,0 +1,5 @@\n+{\n+  \"type\": \"bugfix\",\n+  \"category\": \"ManagedUpload\",\n+  \"description\": \"fix a bug that credentials refresh to frequently\"",
        "comment_created_at": "2021-04-07T17:14:07+00:00",
        "comment_author": "trivikr",
        "comment_body": "The type already has bugfix\r\n```suggestion\r\n  \"description\": \"Use resolved credentials if customer supplies configured S3 Client\"\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
