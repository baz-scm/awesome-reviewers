---
title: Complete configuration type definitions
description: Ensure configuration type definitions are complete and consistent between
  global and service-specific settings. When designing configuration classes, include
  service identifiers as optional instance variables and ensure update methods accept
  all relevant option types that might be used at both global and service-specific
  levels.
repository: aws/aws-sdk-js
label: Configurations
language: Typescript
comments_count: 2
repository_stars: 7628
---

Ensure configuration type definitions are complete and consistent between global and service-specific settings. When designing configuration classes, include service identifiers as optional instance variables and ensure update methods accept all relevant option types that might be used at both global and service-specific levels.

Example:
```typescript
// Proper configuration class definition
export class Config {
  // Service identifiers as optional properties
  s3?: ServiceConfigurationOptions;
  dynamodb?: ServiceConfigurationOptions;
  
  // Update method that accepts all relevant option types
  update(options: ConfigurationOptions & 
         ConfigurationServicePlaceholders & 
         APIVersions & 
         CredentialsOptions, 
         allowUnknownKeys?: boolean): void;
}

// Usage example
AWS.config.s3 = {params: {Bucket: 'myBucket'}, useDualstack: true};
```

This approach prevents TypeScript compiler errors when users set valid configurations and maintains consistency between global and service-specific configuration options.


[
  {
    "discussion_id": "85628177",
    "pr_number": 1189,
    "pr_file": "lib/config.d.ts",
    "created_at": "2016-10-29T00:12:56+00:00",
    "commented_code": "/// <reference types=\"node\" />\n\nimport * as http from 'http';\nimport * as https from 'https';\nimport {AWSError} from './error';\nimport {Credentials} from './credentials';\nexport class Config {",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "85628177",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1189,
        "pr_file": "lib/config.d.ts",
        "discussion_id": "85628177",
        "commented_code": "@@ -0,0 +1,268 @@\n+/// <reference types=\"node\" />\n+\n+import * as http from 'http';\n+import * as https from 'https';\n+import {AWSError} from './error';\n+import {Credentials} from './credentials';\n+export class Config {",
        "comment_created_at": "2016-10-29T00:12:56+00:00",
        "comment_author": "LiuJoyceC",
        "comment_body": "The `Config` class also needs to have each service identifier as an optional instance variable. Otherwise the compiler will complain if a user tries to define service-specific parameters and options:\n\n```\nAWS.config.s3 = {params: {Bucket: 'myBucket'}, useDualstack: true};\n```\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "94810141",
    "pr_number": 1285,
    "pr_file": "lib/config.d.ts",
    "created_at": "2017-01-05T17:18:54+00:00",
    "commented_code": "* @param {ConfigurationOptions} options - a map of option keys and values.\n     * @param {boolean} allowUnknownKeys - Whether unknown keys can be set on the configuration object.\n     */\n    update(options: ConfigurationOptions & ConfigurationServicePlaceholders & APIVersions & {[key: string]: any}, allowUnknownKeys: true): void;\n    update(options: ConfigurationOptions & ConfigurationServicePlaceholders & APIVersions & CredentialsOptions & {[key: string]: any}, allowUnknownKeys: true): void;\n    /**\n     * Updates the current configuration object with new options.\n     * \n     * @param {ConfigurationOptions} options - a map of option keys and values.\n     * @param {boolean} allowUnknownKeys - Defaults to false. Whether unknown keys can be set on the configuration object.\n     */\n    update(options: ConfigurationOptions & ConfigurationServicePlaceholders & APIVersions, allowUnknownKeys?: false): void;\n    update(options: ConfigurationOptions & ConfigurationServicePlaceholders & APIVersions & CredentialsOptions, allowUnknownKeys?: false): void;",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "94810141",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 1285,
        "pr_file": "lib/config.d.ts",
        "discussion_id": "94810141",
        "commented_code": "@@ -63,14 +63,14 @@ export class Config extends ConfigBase {\n      * @param {ConfigurationOptions} options - a map of option keys and values.\n      * @param {boolean} allowUnknownKeys - Whether unknown keys can be set on the configuration object.\n      */\n-    update(options: ConfigurationOptions & ConfigurationServicePlaceholders & APIVersions & {[key: string]: any}, allowUnknownKeys: true): void;\n+    update(options: ConfigurationOptions & ConfigurationServicePlaceholders & APIVersions & CredentialsOptions & {[key: string]: any}, allowUnknownKeys: true): void;\n     /**\n      * Updates the current configuration object with new options.\n      * \n      * @param {ConfigurationOptions} options - a map of option keys and values.\n      * @param {boolean} allowUnknownKeys - Defaults to false. Whether unknown keys can be set on the configuration object.\n      */\n-    update(options: ConfigurationOptions & ConfigurationServicePlaceholders & APIVersions, allowUnknownKeys?: false): void;\n+    update(options: ConfigurationOptions & ConfigurationServicePlaceholders & APIVersions & CredentialsOptions, allowUnknownKeys?: false): void;",
        "comment_created_at": "2017-01-05T17:18:54+00:00",
        "comment_author": "chrisradek",
        "comment_body": "Can you add `CredentialsOptions` to the `update` method in `ConfigBase` as well? This should be allowed in service configuration in addition to the global config.",
        "pr_file_module": null
      }
    ]
  }
]
