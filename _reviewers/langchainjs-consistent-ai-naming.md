---
title: Consistent AI naming
description: Use specific and consistent naming conventions when referencing AI services,
  models, and their parameters throughout your codebase. Always include the full provider
  name (e.g., "AzureOpenAI" instead of just "Azure") to clearly distinguish between
  different AI services and avoid ambiguity.
repository: langchain-ai/langchainjs
label: AI
language: Javascript
comments_count: 3
repository_stars: 15004
---

Use specific and consistent naming conventions when referencing AI services, models, and their parameters throughout your codebase. Always include the full provider name (e.g., "AzureOpenAI" instead of just "Azure") to clearly distinguish between different AI services and avoid ambiguity.

For variables, parameters, and properties related to AI services:
- Use fully qualified names that precisely identify the AI provider and service
- Maintain naming consistency across configuration objects, function parameters, and component properties
- Follow established patterns in the codebase for similar AI integrations

Example:
```javascript
// Incorrect - ambiguous naming
const azureParams = `{
  azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
  azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
}`;

// Correct - specific and consistent naming
const azureOpenAIParams = `{
  azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
  azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
  openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"]
}`;

// Component property should also use the specific name
@property {boolean} [hideAzureOpenAI] - Whether or not to hide Microsoft Azure OpenAI chat model.
```

This practice improves code readability, reduces confusion when working with multiple AI services, and makes maintenance easier, especially as you integrate additional AI providers in the future.


[
  {
    "discussion_id": "2063484090",
    "pr_number": 5624,
    "pr_file": "docs/core_docs/src/theme/ChatModelTabs.js",
    "created_at": "2025-04-28T11:39:51+00:00",
    "commented_code": "mistralParams: `{\\n  model: \"mistral-large-latest\",\\n  temperature: 0\\n}`,\n  groqParams: `{\\n  model: \"llama-3.3-70b-versatile\",\\n  temperature: 0\\n}`,\n  vertexParams: `{\\n  model: \"gemini-1.5-flash\",\\n  temperature: 0\\n}`,\n    azureParams: `{\\n  azure_endpoint=os.environ[\"AZURE_OPENAI_ENDPOINT\"],\\n  azure_deployment=os.environ[\"AZURE_OPENAI_DEPLOYMENT_NAME\"],\\n  openai_api_version=os.environ[\"AZURE_OPENAI_API_VERSION\"]\\n}`,",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2063484090",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5624,
        "pr_file": "docs/core_docs/src/theme/ChatModelTabs.js",
        "discussion_id": "2063484090",
        "commented_code": "@@ -31,6 +31,7 @@ const DEFAULTS = {\n   mistralParams: `{\\n  model: \"mistral-large-latest\",\\n  temperature: 0\\n}`,\n   groqParams: `{\\n  model: \"llama-3.3-70b-versatile\",\\n  temperature: 0\\n}`,\n   vertexParams: `{\\n  model: \"gemini-1.5-flash\",\\n  temperature: 0\\n}`,\n+    azureParams: `{\\n  azure_endpoint=os.environ[\"AZURE_OPENAI_ENDPOINT\"],\\n  azure_deployment=os.environ[\"AZURE_OPENAI_DEPLOYMENT_NAME\"],\\n  openai_api_version=os.environ[\"AZURE_OPENAI_API_VERSION\"]\\n}`,",
        "comment_created_at": "2025-04-28T11:39:51+00:00",
        "comment_author": "benjamincburns",
        "comment_body": "```suggestion\r\n  vertexParams: `{\\n  model: \"gemini-1.5-flash\",\\n  temperature: 0\\n}`,\r\n  azureParams: `{\\n  azure_endpoint=os.environ[\"AZURE_OPENAI_ENDPOINT\"],\\n  azure_deployment=os.environ[\"AZURE_OPENAI_DEPLOYMENT_NAME\"],\\n  openai_api_version=os.environ[\"AZURE_OPENAI_API_VERSION\"]\\n}`,\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2063490565",
    "pr_number": 5624,
    "pr_file": "docs/core_docs/src/theme/ChatModelTabs.js",
    "created_at": "2025-04-28T11:44:33+00:00",
    "commented_code": "envs: `ANTHROPIC_API_KEY=your-api-key`,\n      dependencies: \"@langchain/anthropic\",\n    },\n    azure: {\n      value: \"azure\",\n      label: \"Azure\",\n      default: false,\n      text: `import { AzureChatOpenAI } from \"@langchain/openai\";\\n\\nconst ${llmVarName} = new AzureChatOpenAI(${azureParams});`,",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2063490565",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5624,
        "pr_file": "docs/core_docs/src/theme/ChatModelTabs.js",
        "discussion_id": "2063490565",
        "commented_code": "@@ -95,6 +99,14 @@ export default function ChatModelTabs(props) {\n       envs: `ANTHROPIC_API_KEY=your-api-key`,\n       dependencies: \"@langchain/anthropic\",\n     },\n+    azure: {\n+      value: \"azure\",\n+      label: \"Azure\",\n+      default: false,\n+      text: `import { AzureChatOpenAI } from \"@langchain/openai\";\\n\\nconst ${llmVarName} = new AzureChatOpenAI(${azureParams});`,",
        "comment_created_at": "2025-04-28T11:44:33+00:00",
        "comment_author": "benjamincburns",
        "comment_body": "```suggestion\r\n      text: `import { AzureChatOpenAI } from \"@langchain/openai\";\\n\\nconst ${llmVarName} = new AzureChatOpenAI(${azureOpenAIParams});`,\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2063494283",
    "pr_number": 5624,
    "pr_file": "docs/core_docs/src/theme/ChatModelTabs.js",
    "created_at": "2025-04-28T11:46:54+00:00",
    "commented_code": "*\n * @property {boolean} [hideOpenai] - Whether or not to hide OpenAI chat model.\n * @property {boolean} [hideAnthropic] - Whether or not to hide Anthropic chat model.\n * @property {boolean} [hideAzure] - Whether or not to hide Microsoft Azure OpenAI chat model.",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2063494283",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5624,
        "pr_file": "docs/core_docs/src/theme/ChatModelTabs.js",
        "discussion_id": "2063494283",
        "commented_code": "@@ -46,6 +47,7 @@ const MODELS_WSO = [\"openai\", \"anthropic\", \"mistral\", \"groq\", \"vertex\"];\n  *\n  * @property {boolean} [hideOpenai] - Whether or not to hide OpenAI chat model.\n  * @property {boolean} [hideAnthropic] - Whether or not to hide Anthropic chat model.\n+ * @property {boolean} [hideAzure] - Whether or not to hide Microsoft Azure OpenAI chat model.",
        "comment_created_at": "2025-04-28T11:46:54+00:00",
        "comment_author": "benjamincburns",
        "comment_body": "```suggestion\r\n * @property {boolean} [hideAzureOpenAI] - Whether or not to hide Microsoft Azure OpenAI chat model.\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
