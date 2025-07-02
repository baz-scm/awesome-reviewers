---
title: Dependency classification standards
description: Properly classify dependencies in package.json according to their usage
  pattern and project guidelines. This ensures correct build behavior, optimizes package
  size, and prevents dependency conflicts.
repository: langchain-ai/langchainjs
label: Configurations
language: Json
comments_count: 4
repository_stars: 15004
---

Properly classify dependencies in package.json according to their usage pattern and project guidelines. This ensures correct build behavior, optimizes package size, and prevents dependency conflicts.

- **Direct dependencies**: Include only packages required at runtime
- **Peer dependencies**: Use for optional integrations (also add as dev dependencies for testing)
- **Dev dependencies**: Use for packages only needed during development/testing
- **Avoid unnecessary dependencies**: Don't add packages for functionality available natively

Example of correct dependency classification:
```json
// package.json
{
  "dependencies": {
    // Only runtime requirements
  },
  "peerDependencies": {
    "@libsql/client": "^0.14.0" // Optional integration
  },
  "devDependencies": {
    "@libsql/client": "^0.14.0", // Also needed for testing
    "@cloudflare/workers-types": "^4.20240502.0" // Types only
  }
}
```

For third-party integrations, follow the project's integration guidelines to determine the appropriate dependency type. Avoid adding dependencies when equivalent functionality exists natively.


[
  {
    "discussion_id": "1416502611",
    "pr_number": 3465,
    "pr_file": "langchain/package.json",
    "created_at": "2023-12-06T01:12:43+00:00",
    "commented_code": "\"openai\": \"^4.19.0\",\n    \"openapi-types\": \"^12.1.3\",\n    \"p-retry\": \"4\",\n    \"url\": \"^0.11.3\",",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1416502611",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3465,
        "pr_file": "langchain/package.json",
        "discussion_id": "1416502611",
        "commented_code": "@@ -1445,6 +1453,7 @@\n     \"openai\": \"^4.19.0\",\n     \"openapi-types\": \"^12.1.3\",\n     \"p-retry\": \"4\",\n+    \"url\": \"^0.11.3\",",
        "comment_created_at": "2023-12-06T01:12:43+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "I don't think this is necessary? There is a web built-in",
        "pr_file_module": null
      },
      {
        "comment_id": "1416506907",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3465,
        "pr_file": "langchain/package.json",
        "discussion_id": "1416502611",
        "commented_code": "@@ -1445,6 +1453,7 @@\n     \"openai\": \"^4.19.0\",\n     \"openapi-types\": \"^12.1.3\",\n     \"p-retry\": \"4\",\n+    \"url\": \"^0.11.3\",",
        "comment_created_at": "2023-12-06T01:16:20+00:00",
        "comment_author": "oscarchen178",
        "comment_body": "yep, no need, I will remove this",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1868462212",
    "pr_number": 7253,
    "pr_file": "libs/langchain-community/package.json",
    "created_at": "2024-12-03T22:47:44+00:00",
    "commented_code": "\"author\": \"LangChain\",\n  \"license\": \"MIT\",\n  \"dependencies\": {\n    \"@hashgraph/sdk\": \"^2.53.0\",",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1868462212",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7253,
        "pr_file": "libs/langchain-community/package.json",
        "discussion_id": "1868462212",
        "commented_code": "@@ -35,6 +35,7 @@\n   \"author\": \"LangChain\",\n   \"license\": \"MIT\",\n   \"dependencies\": {\n+    \"@hashgraph/sdk\": \"^2.53.0\",",
        "comment_created_at": "2024-12-03T22:47:44+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Should be a peer + dev dep, not a direct dependency:\r\n\r\nhttps://github.com/langchain-ai/langchainjs/blob/main/.github/contributing/INTEGRATIONS.md#third-party-dependencies",
        "pr_file_module": null
      },
      {
        "comment_id": "1883296405",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7253,
        "pr_file": "libs/langchain-community/package.json",
        "discussion_id": "1868462212",
        "commented_code": "@@ -35,6 +35,7 @@\n   \"author\": \"LangChain\",\n   \"license\": \"MIT\",\n   \"dependencies\": {\n+    \"@hashgraph/sdk\": \"^2.53.0\",",
        "comment_created_at": "2024-12-13T05:03:56+00:00",
        "comment_author": "syntaxsec",
        "comment_body": "Will be done by EOD Monday. Are there any other changes we need to make? ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1788322743",
    "pr_number": 6904,
    "pr_file": "libs/langchain-community/package.json",
    "created_at": "2024-10-04T21:05:08+00:00",
    "commented_code": "\"@langchain/scripts\": \">=0.1.0 <0.2.0\",\n    \"@langchain/standard-tests\": \"0.0.0\",\n    \"@layerup/layerup-security\": \"^1.5.12\",\n    \"@libsql/client\": \"^0.14.0\",",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1788322743",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6904,
        "pr_file": "libs/langchain-community/package.json",
        "discussion_id": "1788322743",
        "commented_code": "@@ -82,6 +82,7 @@\n     \"@langchain/scripts\": \">=0.1.0 <0.2.0\",\n     \"@langchain/standard-tests\": \"0.0.0\",\n     \"@layerup/layerup-security\": \"^1.5.12\",\n+    \"@libsql/client\": \"^0.14.0\",",
        "comment_created_at": "2024-10-04T21:05:08+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "This also should be an optional peer dep:\r\n\r\nhttps://js.langchain.com/docs/contributing/code/#adding-an-entrypoint",
        "pr_file_module": null
      },
      {
        "comment_id": "1789879845",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6904,
        "pr_file": "libs/langchain-community/package.json",
        "discussion_id": "1788322743",
        "commented_code": "@@ -82,6 +82,7 @@\n     \"@langchain/scripts\": \">=0.1.0 <0.2.0\",\n     \"@langchain/standard-tests\": \"0.0.0\",\n     \"@layerup/layerup-security\": \"^1.5.12\",\n+    \"@libsql/client\": \"^0.14.0\",",
        "comment_created_at": "2024-10-07T09:40:03+00:00",
        "comment_author": "notrab",
        "comment_body": "Added",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1591312677",
    "pr_number": 5287,
    "pr_file": "libs/langchain-cloudflare/package.json",
    "created_at": "2024-05-06T17:06:25+00:00",
    "commented_code": "\"author\": \"LangChain\",\n  \"license\": \"MIT\",\n  \"dependencies\": {\n    \"@cloudflare/ai\": \"^1.0.47\",\n    \"@langchain/core\": \"~0.1\",\n    \"uuid\": \"^9.0.1\"\n  },\n  \"devDependencies\": {\n    \"@cloudflare/workers-types\": \"^4.20231218.0\",\n    \"@cloudflare/workers-types\": \"^4.20240502.0\",",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1591312677",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5287,
        "pr_file": "libs/langchain-cloudflare/package.json",
        "discussion_id": "1591312677",
        "commented_code": "@@ -38,12 +38,11 @@\n   \"author\": \"LangChain\",\n   \"license\": \"MIT\",\n   \"dependencies\": {\n-    \"@cloudflare/ai\": \"^1.0.47\",\n     \"@langchain/core\": \"~0.1\",\n     \"uuid\": \"^9.0.1\"\n   },\n   \"devDependencies\": {\n-    \"@cloudflare/workers-types\": \"^4.20231218.0\",\n+    \"@cloudflare/workers-types\": \"^4.20240502.0\",",
        "comment_created_at": "2024-05-06T17:06:25+00:00",
        "comment_author": "bracesproul",
        "comment_body": "If we're replacing `@cloudflare/ai` with this, it needs to be moved out of dev deps and into standard deps",
        "pr_file_module": null
      },
      {
        "comment_id": "1591350680",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5287,
        "pr_file": "libs/langchain-cloudflare/package.json",
        "discussion_id": "1591312677",
        "commented_code": "@@ -38,12 +38,11 @@\n   \"author\": \"LangChain\",\n   \"license\": \"MIT\",\n   \"dependencies\": {\n-    \"@cloudflare/ai\": \"^1.0.47\",\n     \"@langchain/core\": \"~0.1\",\n     \"uuid\": \"^9.0.1\"\n   },\n   \"devDependencies\": {\n-    \"@cloudflare/workers-types\": \"^4.20231218.0\",\n+    \"@cloudflare/workers-types\": \"^4.20240502.0\",",
        "comment_created_at": "2024-05-06T17:44:22+00:00",
        "comment_author": "Cherry",
        "comment_body": "`workers-types` only provides the types for the `Ai` binding - there's nothing runtime that would need this to be a dependency and not a devDependency. The runtime for the AI binding is handled entirely in workerd via wrangler.",
        "pr_file_module": null
      }
    ]
  }
]
