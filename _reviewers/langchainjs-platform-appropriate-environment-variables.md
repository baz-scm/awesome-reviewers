---
title: Platform-appropriate environment variables
description: Always use the correct syntax for accessing environment variables based
  on the target platform. In JavaScript/Node.js environments, use `process.env.VARIABLE_NAME`
  instead of syntaxes from other languages (e.g., Python's `os.environ`).
repository: langchain-ai/langchainjs
label: Configurations
language: Javascript
comments_count: 2
repository_stars: 15004
---

Always use the correct syntax for accessing environment variables based on the target platform. In JavaScript/Node.js environments, use `process.env.VARIABLE_NAME` instead of syntaxes from other languages (e.g., Python's `os.environ`).

Example:
```javascript
// Incorrect - Using Python syntax in JavaScript
const config = {
  azure_endpoint: os.environ["AZURE_OPENAI_ENDPOINT"],
  azure_deployment: os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
  openai_api_version: os.environ["AZURE_OPENAI_API_VERSION"]
};

// Correct - Using JavaScript syntax
const config = {
  azure_endpoint: process.env.AZURE_OPENAI_ENDPOINT,
  azure_deployment: process.env.AZURE_OPENAI_DEPLOYMENT_NAME,
  openai_api_version: process.env.AZURE_OPENAI_API_VERSION
};
```

For platform-specific configurations, consider using appropriate file formats (like .mdx for Node-specific code) or implement automatic import methods that work across environments to improve compatibility.


[
  {
    "discussion_id": "1653253310",
    "pr_number": 5624,
    "pr_file": "docs/core_docs/src/theme/ChatModelTabs.js",
    "created_at": "2024-06-25T17:27:15+00:00",
    "commented_code": "mistralParams: `{\\n  model: \"mistral-large-latest\",\\n  temperature: 0\\n}`,\n  groqParams: `{\\n  model: \"mixtral-8x7b-32768\",\\n  temperature: 0\\n}`,\n  vertexParams: `{\\n  model: \"gemini-1.5-pro\",\\n  temperature: 0\\n}`,\n  azureParams: `{\\n  azure_endpoint=os.environ[\"AZURE_OPENAI_ENDPOINT\"],\\n  azure_deployment=os.environ[\"AZURE_OPENAI_DEPLOYMENT_NAME\"],\\n  openai_api_version=os.environ[\"AZURE_OPENAI_API_VERSION\"]\\n}`,",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1653253310",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5624,
        "pr_file": "docs/core_docs/src/theme/ChatModelTabs.js",
        "discussion_id": "1653253310",
        "commented_code": "@@ -31,6 +31,7 @@ const DEFAULTS = {\n   mistralParams: `{\\n  model: \"mistral-large-latest\",\\n  temperature: 0\\n}`,\n   groqParams: `{\\n  model: \"mixtral-8x7b-32768\",\\n  temperature: 0\\n}`,\n   vertexParams: `{\\n  model: \"gemini-1.5-pro\",\\n  temperature: 0\\n}`,\n+  azureParams: `{\\n  azure_endpoint=os.environ[\"AZURE_OPENAI_ENDPOINT\"],\\n  azure_deployment=os.environ[\"AZURE_OPENAI_DEPLOYMENT_NAME\"],\\n  openai_api_version=os.environ[\"AZURE_OPENAI_API_VERSION\"]\\n}`,",
        "comment_created_at": "2024-06-25T17:27:15+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "JavaScript uses `process.env`",
        "pr_file_module": null
      },
      {
        "comment_id": "2063486552",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5624,
        "pr_file": "docs/core_docs/src/theme/ChatModelTabs.js",
        "discussion_id": "1653253310",
        "commented_code": "@@ -31,6 +31,7 @@ const DEFAULTS = {\n   mistralParams: `{\\n  model: \"mistral-large-latest\",\\n  temperature: 0\\n}`,\n   groqParams: `{\\n  model: \"mixtral-8x7b-32768\",\\n  temperature: 0\\n}`,\n   vertexParams: `{\\n  model: \"gemini-1.5-pro\",\\n  temperature: 0\\n}`,\n+  azureParams: `{\\n  azure_endpoint=os.environ[\"AZURE_OPENAI_ENDPOINT\"],\\n  azure_deployment=os.environ[\"AZURE_OPENAI_DEPLOYMENT_NAME\"],\\n  openai_api_version=os.environ[\"AZURE_OPENAI_API_VERSION\"]\\n}`,",
        "comment_created_at": "2025-04-28T11:41:37+00:00",
        "comment_author": "benjamincburns",
        "comment_body": "```suggestion\r\n  azureParams: `{\\n  azure_endpoint=process.env.AZURE_OPENAI_ENDPOINT,\\n  azure_deployment=process.env.AZURE_OPENAI_DEPLOYMENT_NAME,\\n  openai_api_version=process.env.AZURE_OPENAI_API_VERSION\\n}`,\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1438352901",
    "pr_number": 3794,
    "pr_file": "docs/core_docs/scripts/notebook_init_utils.js",
    "created_at": "2023-12-29T17:46:14+00:00",
    "commented_code": "/* eslint-disable */",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1438352901",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3794,
        "pr_file": "docs/core_docs/scripts/notebook_init_utils.js",
        "discussion_id": "1438352901",
        "commented_code": "@@ -0,0 +1,11 @@\n+/* eslint-disable */",
        "comment_created_at": "2023-12-29T17:46:14+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Yeah let's cut these if we can't find an automatic way to import them. If we really need something Node specific we can just use `.mdx`\r\n\r\nI can also reach out to the Deno team to see if they have suggestions, we have a channel with them.",
        "pr_file_module": null
      }
    ]
  }
]
