---
title: Accurate type signatures
description: 'When defining API interfaces in TypeScript, ensure that method signatures
  accurately reflect the actual behavior and requirements of the implementation. Pay
  special attention to:'
repository: aws/aws-sdk-js
label: API
language: Typescript
comments_count: 2
repository_stars: 7628
---

When defining API interfaces in TypeScript, ensure that method signatures accurately reflect the actual behavior and requirements of the implementation. Pay special attention to:

1. Parameter optionality: Consider carefully whether parameters should be optional (`param?:`) or required based on their usage patterns. If a callback is expected to be called in most use cases, it might be better to make it required to guide developers toward correct usage.

2. Promise return types: Methods that return promises must specify the correct type of the resolved value. Never use `Promise<void>` when the promise actually resolves to a useful value.

Example of correcting return type:
```typescript
// Incorrect
getSignedUrlPromise(operation: string, params: any): Promise<void>;

// Correct 
getSignedUrlPromise(operation: string, params: any): Promise<string>;
```

Example of parameter optionality consideration:
```typescript
// With optional callback - allows but doesn't enforce callback usage
on(event: "validate", listener: (request: Request<D, E>, doneCallback?: () => void) => void): Request<D, E>;

// With required callback - enforces callback usage for correct implementation
on(event: "validate", listener: (request: Request<D, E>, doneCallback: () => void) => void): Request<D, E>;
```

Accurate type signatures improve API usability, enable better IDE support, and reduce runtime errors by catching incorrect usage patterns at compile time.


[
  {
    "discussion_id": "511436398",
    "pr_number": 3511,
    "pr_file": "lib/request.d.ts",
    "created_at": "2020-10-24T12:46:35+00:00",
    "commented_code": "* @param {function} listener - Callback to run when the request is being validated.\n     * @param {boolean} prepend - If set, prepends listener instead of appending.\n     */\n    on(event: \"validate\", listener: (request: Request<D, E>) => void, prepend?: boolean): Request<D, E>;\n    on(event: \"validate\", listener: (request: Request<D, E>, doneCallback?: () => void) => void, prepend?: boolean): Request<D, E>;",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "511436398",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 3511,
        "pr_file": "lib/request.d.ts",
        "discussion_id": "511436398",
        "commented_code": "@@ -54,23 +54,23 @@ export class Request<D, E> {\n      * @param {function} listener - Callback to run when the request is being validated.\n      * @param {boolean} prepend - If set, prepends listener instead of appending.\n      */\n-    on(event: \"validate\", listener: (request: Request<D, E>) => void, prepend?: boolean): Request<D, E>;\n+    on(event: \"validate\", listener: (request: Request<D, E>, doneCallback?: () => void) => void, prepend?: boolean): Request<D, E>;",
        "comment_created_at": "2020-10-24T12:46:35+00:00",
        "comment_author": "jeromecovington",
        "comment_body": "I added `doneCallback?` as an optional second param, trying to be sensitive to not breaking anybody's current code that may not use the param. Although I'm divided on whether or not it should probably actually be a required argument, as I'm not sure anyone's code using `onAsync()` listeners should technically be correct _without_ calling `done()`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "145172099",
    "pr_number": 1711,
    "pr_file": "lib/services/s3.d.ts",
    "created_at": "2017-10-17T15:45:27+00:00",
    "commented_code": "getSignedUrl(operation: string, params: any): string;\n\n    /**\n     * Returns a 'thenable' promise that will be resolved with a pre-signed URL for a given operation name.\n     */\n    getSignedUrlPromise(operation: string, params: any): Promise<void>;",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "145172099",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1711,
        "pr_file": "lib/services/s3.d.ts",
        "discussion_id": "145172099",
        "commented_code": "@@ -13,6 +13,11 @@ export class S3Customizations extends Service {\n     getSignedUrl(operation: string, params: any): string;\n \n     /**\n+     * Returns a 'thenable' promise that will be resolved with a pre-signed URL for a given operation name.\n+     */\n+    getSignedUrlPromise(operation: string, params: any): Promise<void>;",
        "comment_created_at": "2017-10-17T15:45:27+00:00",
        "comment_author": "jeskew",
        "comment_body": "Shouldn't the return value be `Promise<string>`?",
        "pr_file_module": null
      }
    ]
  }
]
