---
title: Consistent naming conventions
description: 'Maintain consistent and explicit naming conventions across your codebase
  that reflect:


  1. **Component dependencies**: Class/function names should explicitly indicate their
  external dependencies and integrations to improve clarity and avoid confusion.'
repository: langchain-ai/langchainjs
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 15004
---

Maintain consistent and explicit naming conventions across your codebase that reflect:

1. **Component dependencies**: Class/function names should explicitly indicate their external dependencies and integrations to improve clarity and avoid confusion.
   ```typescript
   // INCORRECT: Doesn't indicate dependency on Unstructured API
   class DropboxLoader { ... }
   
   // CORRECT: Explicitly indicates dependency
   class DropboxUnstructuredLoader { ... }
   ```

2. **Current parameter naming**: Use the current preferred parameter names rather than deprecated ones, and be consistent across all instances.
   ```javascript
   // INCORRECT: Using deprecated parameter name
   const model = new ChatOpenAI({
     modelName: "gpt-azure",
   });
   
   // CORRECT: Using current parameter name
   const model = new ChatOpenAI({
     model: "gpt-azure",
   });
   ```

3. **Standard formatting patterns**: Follow standard naming patterns for environment variables and configuration parameters, with proper word separation.
   ```javascript
   // INCORRECT: Concatenated words without separation
   process.env.GOOGLE_DRIVE_CREDENTIALSPATH
   
   // CORRECT: Words properly separated with underscores
   process.env.GOOGLE_DRIVE_CREDENTIALS_PATH
   ```

This consistent approach to naming makes your code more maintainable, reduces confusion for other developers, and provides better clarity about component dependencies and behavior.


[
  {
    "discussion_id": "1896299341",
    "pr_number": 7301,
    "pr_file": "docs/core_docs/docs/integrations/document_loaders/web_loaders/dropbox.mdx",
    "created_at": "2024-12-24T02:26:33+00:00",
    "commented_code": "---\nhide_table_of_contents: true\nsidebar_class_name: node-only\n---\n\n# Dropbox Loader\n\nThe `DropboxLoader` allows you to load documents from Dropbox into your LangChain applications. It retrieves files or directories from your Dropbox account and converts them into documents ready for processing.\n\n## Overview\n\nDropbox is a file hosting service that brings all your files\u2014traditional documents, cloud content, and web shortcuts\u2014together in one place. With the `DropboxLoader`, you can seamlessly integrate Dropbox file retrieval into your projects.\n\n## Setup\n\n1. Create a dropbox app, using the [Dropbox App Console](https://www.dropbox.com/developers/apps/create).\n2. Ensure the app has the `files.metadata.read`, `files.content.read` scope permissions:\n3. Generate the access token from the Dropbox App Console.\n4. To use this loader, you'll need to have Unstructured already set up and ready to use at an available URL endpoint. It can also be configured to run locally.\n   See the docs [here](https://www.dropbox.com/developers/apps/create) for information on how to do that.\n5. Install the necessary packages:\n\n   ```bash npm2yarn\n   npm install @langchain/community @langchain/core dropbox\n   ```\n\n## Usage\n\n### Loading Specific Files\n\nTo load specific files from Dropbox, specify the file paths:\n\n```typescript\nimport { DropboxLoader } from \"@langchain/community/document_loaders/web/dropbox\";\n\nconst loader = new DropboxLoader({\n  clientOptions: {\n    accessToken: \"your-dropbox-access-token\",\n  },\n  unstructuredOptions: {\n    apiUrl: \"http://localhost:8000/general/v0/general\", // Replace with your Unstructured API URL",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1896299341",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7301,
        "pr_file": "docs/core_docs/docs/integrations/document_loaders/web_loaders/dropbox.mdx",
        "discussion_id": "1896299341",
        "commented_code": "@@ -0,0 +1,138 @@\n+---\n+hide_table_of_contents: true\n+sidebar_class_name: node-only\n+---\n+\n+# Dropbox Loader\n+\n+The `DropboxLoader` allows you to load documents from Dropbox into your LangChain applications. It retrieves files or directories from your Dropbox account and converts them into documents ready for processing.\n+\n+## Overview\n+\n+Dropbox is a file hosting service that brings all your files\u2014traditional documents, cloud content, and web shortcuts\u2014together in one place. With the `DropboxLoader`, you can seamlessly integrate Dropbox file retrieval into your projects.\n+\n+## Setup\n+\n+1. Create a dropbox app, using the [Dropbox App Console](https://www.dropbox.com/developers/apps/create).\n+2. Ensure the app has the `files.metadata.read`, `files.content.read` scope permissions:\n+3. Generate the access token from the Dropbox App Console.\n+4. To use this loader, you'll need to have Unstructured already set up and ready to use at an available URL endpoint. It can also be configured to run locally.\n+   See the docs [here](https://www.dropbox.com/developers/apps/create) for information on how to do that.\n+5. Install the necessary packages:\n+\n+   ```bash npm2yarn\n+   npm install @langchain/community @langchain/core dropbox\n+   ```\n+\n+## Usage\n+\n+### Loading Specific Files\n+\n+To load specific files from Dropbox, specify the file paths:\n+\n+```typescript\n+import { DropboxLoader } from \"@langchain/community/document_loaders/web/dropbox\";\n+\n+const loader = new DropboxLoader({\n+  clientOptions: {\n+    accessToken: \"your-dropbox-access-token\",\n+  },\n+  unstructuredOptions: {\n+    apiUrl: \"http://localhost:8000/general/v0/general\", // Replace with your Unstructured API URL",
        "comment_created_at": "2024-12-24T02:26:33+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Let's emphasize somewhere that this wraps Unstructured\r\n\r\nShould we call this `DropboxUnstructuredLoader` instead?",
        "pr_file_module": null
      },
      {
        "comment_id": "1900509302",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7301,
        "pr_file": "docs/core_docs/docs/integrations/document_loaders/web_loaders/dropbox.mdx",
        "discussion_id": "1896299341",
        "commented_code": "@@ -0,0 +1,138 @@\n+---\n+hide_table_of_contents: true\n+sidebar_class_name: node-only\n+---\n+\n+# Dropbox Loader\n+\n+The `DropboxLoader` allows you to load documents from Dropbox into your LangChain applications. It retrieves files or directories from your Dropbox account and converts them into documents ready for processing.\n+\n+## Overview\n+\n+Dropbox is a file hosting service that brings all your files\u2014traditional documents, cloud content, and web shortcuts\u2014together in one place. With the `DropboxLoader`, you can seamlessly integrate Dropbox file retrieval into your projects.\n+\n+## Setup\n+\n+1. Create a dropbox app, using the [Dropbox App Console](https://www.dropbox.com/developers/apps/create).\n+2. Ensure the app has the `files.metadata.read`, `files.content.read` scope permissions:\n+3. Generate the access token from the Dropbox App Console.\n+4. To use this loader, you'll need to have Unstructured already set up and ready to use at an available URL endpoint. It can also be configured to run locally.\n+   See the docs [here](https://www.dropbox.com/developers/apps/create) for information on how to do that.\n+5. Install the necessary packages:\n+\n+   ```bash npm2yarn\n+   npm install @langchain/community @langchain/core dropbox\n+   ```\n+\n+## Usage\n+\n+### Loading Specific Files\n+\n+To load specific files from Dropbox, specify the file paths:\n+\n+```typescript\n+import { DropboxLoader } from \"@langchain/community/document_loaders/web/dropbox\";\n+\n+const loader = new DropboxLoader({\n+  clientOptions: {\n+    accessToken: \"your-dropbox-access-token\",\n+  },\n+  unstructuredOptions: {\n+    apiUrl: \"http://localhost:8000/general/v0/general\", // Replace with your Unstructured API URL",
        "comment_created_at": "2025-01-02T02:53:15+00:00",
        "comment_author": "Ser0n-ath",
        "comment_body": "Yes, we can rename the loader class to `DropboxUnstructuredLoader`\r\nI want to confirm if I need to rename the file to say `dropbox_unstructured.ts` as well?\r\n\r\nAlso, I noticed that a few preexisting loaders utilize unstructured as well. Would they need to be renamed as well in the future?:\r\n- [s3](https://github.com/langchain-ai/langchainjs/blob/main/libs/langchain-community/src/document_loaders/web/s3.ts)\r\n- [azure_blob_storage](https://github.com/langchain-ai/langchainjs/blob/main/libs/langchain-community/src/document_loaders/web/azure_blob_storage_file.ts)\r\n\r\n\r\n\r\n\r\n\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1690477167",
    "pr_number": 6197,
    "pr_file": "docs/core_docs/docs/integrations/chat/litellm_proxy.mdx",
    "created_at": "2024-07-24T21:29:52+00:00",
    "commented_code": "---\nsidebar_label: LiteLLM Proxy\n---\n\nimport CodeBlock from \"@theme/CodeBlock\";\n\n# LiteLLM Proxy Server\n\nUse [LiteLLM Proxy](https://docs.litellm.ai/docs/simple_proxy) for:\n\n- Calling 100+ LLMs OpenAI, Azure, Vertex, Bedrock/etc using OpenAI format\n- Use Virtual Keys to Set Budgets & Track Usage\n\nThis allows you to call 100+ LLMs using `ChatOpenAI`\n\n```js\nimport { ChatOpenAI } from \"@langchain/openai\";\n\nconst model = new ChatOpenAI({\n  modelName: \"claude-3-5-sonnet-20240620\", // swap this for \"gpt-4o-mini\", \"gemini-1.5-pro\", \"claude-3-5-sonnet-20240620\"\n  openAIApiKey: \"sk-1234\",\n}, {\n  basePath: \"http://0.0.0.0:4000\", // set basePath to LiteLLM Proxy server\n});\n\nconst message = await model.invoke(\"Hi there!\");\n\nconsole.log(message);\n```\n\n\n## Step 1 Setup LiteLLM Proxy config.yaml\n\nLiteLLM Requires a config with all your models defined - we can call this file `litellm_config.yaml`\n\n[Detailed docs on how to setup litellm config - here](https://docs.litellm.ai/docs/proxy/configs)\n\n```yaml\nmodel_list:\n  # Azure OpenAI\n  # https://docs.litellm.ai/docs/providers/azure\n  - model_name: gpt-azure\n    litellm_params:\n      model: azure/gpt-turbo-small-ca\n      api_base: https://my-endpoint-canada-berri992.openai.azure.com/\n      api_key: \"os.environ/AZURE_API_KEY\"\n\n  # OpenAI API\n  # https://docs.litellm.ai/docs/providers/openai\n  - model_name: gpt-4o-mini\n    litellm_params:\n      model: openai/gpt-4o-mini\n      api_key: \"os.environ/OPENAI_API_KEY\"\n\n\n  # Vertex AI models\n  # https://docs.litellm.ai/docs/providers/vertex\n  - model_name: gemini-pro\n    litellm_params:\n      model: vertex_ai_beta/gemini-1.5-pro\n      vertex_project: \"project-id\"\n      vertex_location: \"us-central1\"\n      vertex_credentials: \"/path/to/service_account.json\" # [OPTIONAL] Do this OR `!gcloud auth application-default login` - run this to add vertex credentials to your env\n  \n  # Bedrock Models\n  # https://docs.litellm.ai/docs/providers/bedrock\n  - model_name: anthropic-claude\n    litellm_params: \n      model: bedrock/anthropic.claude-instant-v1\n      aws_access_key_id: os.environ/CUSTOM_AWS_ACCESS_KEY_ID\n      aws_secret_access_key: os.environ/CUSTOM_AWS_SECRET_ACCESS_KEY\n      aws_region_name: os.environ/CUSTOM_AWS_REGION_NAME\n  \n```\n\n\n## Step 2. Start litellm proxy\n\n```shell\ndocker run \\\n    -v $(pwd)/litellm_config.yaml:/app/config.yaml \\\n    -p 4000:4000 \\\n    -e AZURE_API_KEY \\\n    -e OPENAI_API_KEY \\\n    -e CUSTOM_AWS_ACCESS_KEY_ID \\\n    -e CUSTOM_AWS_SECRET_ACCESS_KEY \\\n    -e CUSTOM_AWS_REGION_NAME \\\n    ghcr.io/berriai/litellm:main-latest \\\n    --config /app/config.yaml --detailed_debug\n```\n\nProxy will start running on `http://0.0.0.0:4000/` You can use this endpoint to make all LLM Requests\n\n## Step 3. Make Requests using ChatOpenAI\n\nWe use Langchain JS to make requests to LiteLLM Proxy\n\n```bash npm2yarn\nnpm install @langchain/openai\n```\n\nYou can call all models defined on the `litellm_config.yaml`, all you need to do is change the `modelName`\n\n## Call `\"gpt-azure\"`\n```js\nimport { ChatOpenAI } from \"@langchain/openai\";\n\n\nconst model = new ChatOpenAI({\n  modelName: \"gpt-azure\",",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1690477167",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6197,
        "pr_file": "docs/core_docs/docs/integrations/chat/litellm_proxy.mdx",
        "discussion_id": "1690477167",
        "commented_code": "@@ -0,0 +1,157 @@\n+---\n+sidebar_label: LiteLLM Proxy\n+---\n+\n+import CodeBlock from \"@theme/CodeBlock\";\n+\n+# LiteLLM Proxy Server\n+\n+Use [LiteLLM Proxy](https://docs.litellm.ai/docs/simple_proxy) for:\n+\n+- Calling 100+ LLMs OpenAI, Azure, Vertex, Bedrock/etc using OpenAI format\n+- Use Virtual Keys to Set Budgets & Track Usage\n+\n+This allows you to call 100+ LLMs using `ChatOpenAI`\n+\n+```js\n+import { ChatOpenAI } from \"@langchain/openai\";\n+\n+const model = new ChatOpenAI({\n+  modelName: \"claude-3-5-sonnet-20240620\", // swap this for \"gpt-4o-mini\", \"gemini-1.5-pro\", \"claude-3-5-sonnet-20240620\"\n+  openAIApiKey: \"sk-1234\",\n+}, {\n+  basePath: \"http://0.0.0.0:4000\", // set basePath to LiteLLM Proxy server\n+});\n+\n+const message = await model.invoke(\"Hi there!\");\n+\n+console.log(message);\n+```\n+\n+\n+## Step 1 Setup LiteLLM Proxy config.yaml\n+\n+LiteLLM Requires a config with all your models defined - we can call this file `litellm_config.yaml`\n+\n+[Detailed docs on how to setup litellm config - here](https://docs.litellm.ai/docs/proxy/configs)\n+\n+```yaml\n+model_list:\n+  # Azure OpenAI\n+  # https://docs.litellm.ai/docs/providers/azure\n+  - model_name: gpt-azure\n+    litellm_params:\n+      model: azure/gpt-turbo-small-ca\n+      api_base: https://my-endpoint-canada-berri992.openai.azure.com/\n+      api_key: \"os.environ/AZURE_API_KEY\"\n+\n+  # OpenAI API\n+  # https://docs.litellm.ai/docs/providers/openai\n+  - model_name: gpt-4o-mini\n+    litellm_params:\n+      model: openai/gpt-4o-mini\n+      api_key: \"os.environ/OPENAI_API_KEY\"\n+\n+\n+  # Vertex AI models\n+  # https://docs.litellm.ai/docs/providers/vertex\n+  - model_name: gemini-pro\n+    litellm_params:\n+      model: vertex_ai_beta/gemini-1.5-pro\n+      vertex_project: \"project-id\"\n+      vertex_location: \"us-central1\"\n+      vertex_credentials: \"/path/to/service_account.json\" # [OPTIONAL] Do this OR `!gcloud auth application-default login` - run this to add vertex credentials to your env\n+  \n+  # Bedrock Models\n+  # https://docs.litellm.ai/docs/providers/bedrock\n+  - model_name: anthropic-claude\n+    litellm_params: \n+      model: bedrock/anthropic.claude-instant-v1\n+      aws_access_key_id: os.environ/CUSTOM_AWS_ACCESS_KEY_ID\n+      aws_secret_access_key: os.environ/CUSTOM_AWS_SECRET_ACCESS_KEY\n+      aws_region_name: os.environ/CUSTOM_AWS_REGION_NAME\n+  \n+```\n+\n+\n+## Step 2. Start litellm proxy\n+\n+```shell\n+docker run \\\n+    -v $(pwd)/litellm_config.yaml:/app/config.yaml \\\n+    -p 4000:4000 \\\n+    -e AZURE_API_KEY \\\n+    -e OPENAI_API_KEY \\\n+    -e CUSTOM_AWS_ACCESS_KEY_ID \\\n+    -e CUSTOM_AWS_SECRET_ACCESS_KEY \\\n+    -e CUSTOM_AWS_REGION_NAME \\\n+    ghcr.io/berriai/litellm:main-latest \\\n+    --config /app/config.yaml --detailed_debug\n+```\n+\n+Proxy will start running on `http://0.0.0.0:4000/` You can use this endpoint to make all LLM Requests\n+\n+## Step 3. Make Requests using ChatOpenAI\n+\n+We use Langchain JS to make requests to LiteLLM Proxy\n+\n+```bash npm2yarn\n+npm install @langchain/openai\n+```\n+\n+You can call all models defined on the `litellm_config.yaml`, all you need to do is change the `modelName`\n+\n+## Call `\"gpt-azure\"`\n+```js\n+import { ChatOpenAI } from \"@langchain/openai\";\n+\n+\n+const model = new ChatOpenAI({\n+  modelName: \"gpt-azure\",",
        "comment_created_at": "2024-07-24T21:29:52+00:00",
        "comment_author": "bracesproul",
        "comment_body": "`modelName` is deprecated, prefer `model`\r\n```suggestion\r\nYou can call all models defined on the `litellm_config.yaml`, all you need to do is change the `model` param.\r\n\r\n## Call `\"gpt-azure\"`\r\n```js\r\nimport { ChatOpenAI } from \"@langchain/openai\";\r\n\r\n\r\nconst model = new ChatOpenAI({\r\n  model: \"gpt-azure\",\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1690477573",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6197,
        "pr_file": "docs/core_docs/docs/integrations/chat/litellm_proxy.mdx",
        "discussion_id": "1690477167",
        "commented_code": "@@ -0,0 +1,157 @@\n+---\n+sidebar_label: LiteLLM Proxy\n+---\n+\n+import CodeBlock from \"@theme/CodeBlock\";\n+\n+# LiteLLM Proxy Server\n+\n+Use [LiteLLM Proxy](https://docs.litellm.ai/docs/simple_proxy) for:\n+\n+- Calling 100+ LLMs OpenAI, Azure, Vertex, Bedrock/etc using OpenAI format\n+- Use Virtual Keys to Set Budgets & Track Usage\n+\n+This allows you to call 100+ LLMs using `ChatOpenAI`\n+\n+```js\n+import { ChatOpenAI } from \"@langchain/openai\";\n+\n+const model = new ChatOpenAI({\n+  modelName: \"claude-3-5-sonnet-20240620\", // swap this for \"gpt-4o-mini\", \"gemini-1.5-pro\", \"claude-3-5-sonnet-20240620\"\n+  openAIApiKey: \"sk-1234\",\n+}, {\n+  basePath: \"http://0.0.0.0:4000\", // set basePath to LiteLLM Proxy server\n+});\n+\n+const message = await model.invoke(\"Hi there!\");\n+\n+console.log(message);\n+```\n+\n+\n+## Step 1 Setup LiteLLM Proxy config.yaml\n+\n+LiteLLM Requires a config with all your models defined - we can call this file `litellm_config.yaml`\n+\n+[Detailed docs on how to setup litellm config - here](https://docs.litellm.ai/docs/proxy/configs)\n+\n+```yaml\n+model_list:\n+  # Azure OpenAI\n+  # https://docs.litellm.ai/docs/providers/azure\n+  - model_name: gpt-azure\n+    litellm_params:\n+      model: azure/gpt-turbo-small-ca\n+      api_base: https://my-endpoint-canada-berri992.openai.azure.com/\n+      api_key: \"os.environ/AZURE_API_KEY\"\n+\n+  # OpenAI API\n+  # https://docs.litellm.ai/docs/providers/openai\n+  - model_name: gpt-4o-mini\n+    litellm_params:\n+      model: openai/gpt-4o-mini\n+      api_key: \"os.environ/OPENAI_API_KEY\"\n+\n+\n+  # Vertex AI models\n+  # https://docs.litellm.ai/docs/providers/vertex\n+  - model_name: gemini-pro\n+    litellm_params:\n+      model: vertex_ai_beta/gemini-1.5-pro\n+      vertex_project: \"project-id\"\n+      vertex_location: \"us-central1\"\n+      vertex_credentials: \"/path/to/service_account.json\" # [OPTIONAL] Do this OR `!gcloud auth application-default login` - run this to add vertex credentials to your env\n+  \n+  # Bedrock Models\n+  # https://docs.litellm.ai/docs/providers/bedrock\n+  - model_name: anthropic-claude\n+    litellm_params: \n+      model: bedrock/anthropic.claude-instant-v1\n+      aws_access_key_id: os.environ/CUSTOM_AWS_ACCESS_KEY_ID\n+      aws_secret_access_key: os.environ/CUSTOM_AWS_SECRET_ACCESS_KEY\n+      aws_region_name: os.environ/CUSTOM_AWS_REGION_NAME\n+  \n+```\n+\n+\n+## Step 2. Start litellm proxy\n+\n+```shell\n+docker run \\\n+    -v $(pwd)/litellm_config.yaml:/app/config.yaml \\\n+    -p 4000:4000 \\\n+    -e AZURE_API_KEY \\\n+    -e OPENAI_API_KEY \\\n+    -e CUSTOM_AWS_ACCESS_KEY_ID \\\n+    -e CUSTOM_AWS_SECRET_ACCESS_KEY \\\n+    -e CUSTOM_AWS_REGION_NAME \\\n+    ghcr.io/berriai/litellm:main-latest \\\n+    --config /app/config.yaml --detailed_debug\n+```\n+\n+Proxy will start running on `http://0.0.0.0:4000/` You can use this endpoint to make all LLM Requests\n+\n+## Step 3. Make Requests using ChatOpenAI\n+\n+We use Langchain JS to make requests to LiteLLM Proxy\n+\n+```bash npm2yarn\n+npm install @langchain/openai\n+```\n+\n+You can call all models defined on the `litellm_config.yaml`, all you need to do is change the `modelName`\n+\n+## Call `\"gpt-azure\"`\n+```js\n+import { ChatOpenAI } from \"@langchain/openai\";\n+\n+\n+const model = new ChatOpenAI({\n+  modelName: \"gpt-azure\",",
        "comment_created_at": "2024-07-24T21:30:12+00:00",
        "comment_author": "bracesproul",
        "comment_body": "Please update the rest of the `modelName` instances too.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1414383618",
    "pr_number": 3474,
    "pr_file": "docs/core_docs/docs/integrations/document_loaders/web_loaders/google_drive.mdx",
    "created_at": "2023-12-04T19:24:37+00:00",
    "commented_code": "# Google document loader\n\n## Getting Credentials \n\nhttps://developers.google.com/workspace/guides/get-started#5_steps_to_get_started\nFollow the 5 steps in the above guide to get the credentials to authenticate your app's end users or service accounts.\n\nThen, after getting the right credentials from google, add the file paths to the .env variables GOOGLE_DRIVE_CREDENTIALSPATH and GOOGLE_DRIVE_TOKENPATH",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1414383618",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3474,
        "pr_file": "docs/core_docs/docs/integrations/document_loaders/web_loaders/google_drive.mdx",
        "discussion_id": "1414383618",
        "commented_code": "@@ -0,0 +1,79 @@\n+# Google document loader\n+\n+## Getting Credentials \n+\n+https://developers.google.com/workspace/guides/get-started#5_steps_to_get_started\n+Follow the 5 steps in the above guide to get the credentials to authenticate your app's end users or service accounts.\n+\n+Then, after getting the right credentials from google, add the file paths to the .env variables GOOGLE_DRIVE_CREDENTIALSPATH and GOOGLE_DRIVE_TOKENPATH",
        "comment_created_at": "2023-12-04T19:24:37+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Separate words with underscore:\r\n`GOOGLE_DRIVE_CREDENTIALSPATH` -> `GOOGLE_DRIVE_CREDENTIALS_PATH`",
        "pr_file_module": null
      }
    ]
  }
]
