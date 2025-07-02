---
title: Semantic type organization
description: Organize types and interfaces in intuitive namespace hierarchies and
  use specific types instead of generic ones. Types should be accessible through logically
  related namespaces, and method signatures should accurately reflect their parameters
  and return values. This improves code clarity, discoverability, and type safety.
repository: aws/aws-sdk-js
label: Naming Conventions
language: Typescript
comments_count: 2
repository_stars: 7628
---

Organize types and interfaces in intuitive namespace hierarchies and use specific types instead of generic ones. Types should be accessible through logically related namespaces, and method signatures should accurately reflect their parameters and return values. This improves code clarity, discoverability, and type safety.

```typescript
// Prefer this (specific types, logical organization)
const converter: Converter = DynamoDB.Converter;
function resolvePromise(): Promise<Credentials> { /* ... */ }

// Instead of these (generic types, unintuitive organization)
const converter: any = DynamoDB.Converter;
const options: DynamoDB.DocumentClient.ConverterOptions = { /* ... */ }; // accessing through DocumentClient when logically belongs to Converter
function resolvePromise(): Promise<any> { /* ... */ }
```


[
  {
    "discussion_id": "102779549",
    "pr_number": 1370,
    "pr_file": "ts/dynamodb.ts",
    "created_at": "2017-02-23T18:14:29+00:00",
    "commented_code": "}\n};",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "102779549",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1370,
        "pr_file": "ts/dynamodb.ts",
        "discussion_id": "102779549",
        "commented_code": "@@ -9,6 +9,18 @@ const params: DynamoDB.DocumentClient.GetItemInput = {\n     }\n };\n ",
        "comment_created_at": "2017-02-23T18:14:29+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Can you add tests to make sure we can explicitly set a variable to the `DynamoDB.Converter` type? Also, would be nice to verify we can access `DocumentClient.ConverterOptions`.\r\n\r\nCan be simple, like:\r\n```javascript\r\nconst converter: Converter = DynamoDB.Converter;\r\n// and a test for input with converter options\r\nconst converterOptions: DynamoDB.DocumentClient.ConverterOptions = {convertEmptyValues: true};\r\nDynamoDB.Converter.input('string', converterOptions);\r\n```\r\n\r\nHow hard would it be to also expose ConverterOptions on the Converter namespace? Just feels a little odd having to access it off the DocumentClient namespace instead.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "130689743",
    "pr_number": 1655,
    "pr_file": "lib/credentials/credential_provider_chain.d.ts",
    "created_at": "2017-08-01T18:29:43+00:00",
    "commented_code": "*/\n    resolve(callback:(err: AWSError, credentials: Credentials) => void): CredentialProviderChain;\n    /**\n     * Return a Promise on resolve() function\n     */\n    resolvePromise(resolve?:(credentials: Credentials) => void, reject?:(err: AWSError) => void): Promise<any>;",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "130689743",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1655,
        "pr_file": "lib/credentials/credential_provider_chain.d.ts",
        "discussion_id": "130689743",
        "commented_code": "@@ -10,6 +10,10 @@ export class CredentialProviderChain extends Credentials {\n      */\n     resolve(callback:(err: AWSError, credentials: Credentials) => void): CredentialProviderChain;\n     /**\n+     * Return a Promise on resolve() function\n+     */\n+    resolvePromise(resolve?:(credentials: Credentials) => void, reject?:(err: AWSError) => void): Promise<any>;",
        "comment_created_at": "2017-08-01T18:29:43+00:00",
        "comment_author": "jeskew",
        "comment_body": "This isn't quite right. The return value should use `Credentials` instead of `any`, and the method itself doesn't take any callbacks.",
        "pr_file_module": null
      }
    ]
  }
]
