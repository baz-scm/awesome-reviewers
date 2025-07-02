---
title: Comprehensive AI documentation
description: 'When documenting AI integrations, provide comprehensive examples that
  showcase all common initialization and usage patterns. Documentation should include:'
repository: langchain-ai/langchainjs
label: AI
language: Other
comments_count: 4
repository_stars: 15004
---

When documenting AI integrations, provide comprehensive examples that showcase all common initialization and usage patterns. Documentation should include:

1. All initialization methods (direct constructor, `.fromDocuments`, etc.)
2. Links to related components and services
3. Complete usage examples with different options
4. Adherence to standardized documentation templates

For example, when documenting a vector store integration:

```javascript
// Show direct initialization
const vectorStore = new AIVectorStore(new SomeEmbeddings());

// Also show initialization from documents
const documents = [new Document({ pageContent: "text" })];
const vectorStoreFromDocs = await AIVectorStore.fromDocuments(
  documents,
  new SomeEmbeddings()
);

// Demonstrate common operations
const results = await vectorStore.similaritySearch("query", 5);
```

This practice ensures developers can quickly understand and implement AI integrations without needing to search through multiple documentation pages or source code.


[
  {
    "discussion_id": "1818682202",
    "pr_number": 7033,
    "pr_file": "docs/core_docs/docs/integrations/platforms/microsoft.mdx",
    "created_at": "2024-10-28T09:23:11+00:00",
    "commented_code": "import { AzureCosmosDBMongoDBVectorStore } from \"@langchain/azure-cosmosdb\";\n```\n\n## Semantic Cache\n\n### Azure Cosmos DB NoSQL Semantic Cache\n\n> The Semantic Cache feature is supported with Azure Cosmos DB for NoSQL integration, enabling users to retrieve cached responses based on semantic similarity between the user input and previously cached results. It leverages AzureCosmosDBNoSQLVectorStore, which stores vector embeddings of cached prompts. These embeddings enable similarity-based searches, allowing the system to retrieve relevant cached results.",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1818682202",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7033,
        "pr_file": "docs/core_docs/docs/integrations/platforms/microsoft.mdx",
        "discussion_id": "1818682202",
        "commented_code": "@@ -132,6 +132,24 @@ See a [usage example](/docs/integrations/vectorstores/azure_cosmosdb_mongodb).\n import { AzureCosmosDBMongoDBVectorStore } from \"@langchain/azure-cosmosdb\";\n ```\n \n+## Semantic Cache\n+\n+### Azure Cosmos DB NoSQL Semantic Cache\n+\n+> The Semantic Cache feature is supported with Azure Cosmos DB for NoSQL integration, enabling users to retrieve cached responses based on semantic similarity between the user input and previously cached results. It leverages AzureCosmosDBNoSQLVectorStore, which stores vector embeddings of cached prompts. These embeddings enable similarity-based searches, allowing the system to retrieve relevant cached results.",
        "comment_created_at": "2024-10-28T09:23:11+00:00",
        "comment_author": "sinedied",
        "comment_body": "nit: a link to `AzureCosmosDBNoSQLVectorStore` doc would be nice here",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1705945143",
    "pr_number": 6414,
    "pr_file": "docs/core_docs/docs/integrations/vectorstores/memory.ipynb",
    "created_at": "2024-08-06T18:21:09+00:00",
    "commented_code": "{\n \"cells\": [\n  {\n   \"cell_type\": \"raw\",\n   \"id\": \"1957f5cb\",\n   \"metadata\": {\n    \"vscode\": {\n     \"languageId\": \"raw\"\n    }\n   },\n   \"source\": [\n    \"---\\n\",\n    \"sidebar_label: In Memory\\n\",\n    \"---\"\n   ]\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"ef1f0986\",\n   \"metadata\": {},\n   \"source\": [\n    \"# MemoryVectorStore\\n\",\n    \"\\n\",\n    \"MemoryVectorStore is an in-memory, ephemeral vectorstore that stores embeddings in-memory and does an exact, linear search for the most similar embeddings. The default similarity metric is cosine similarity, but can be changed to any of the similarity metrics supported by [ml-distance](https://mljs.github.io/distance/modules/similarity.html).\\n\"\n   ]\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"36fdc060\",\n   \"metadata\": {},\n   \"source\": [\n    \"## Setup\\n\",\n    \"\\n\",\n    \"To access the in memory vector store you'll need to install the `langchain` integration package.\\n\",\n    \"\\n\",\n    \"```{=mdx}\\n\",\n    \"import IntegrationInstallTooltip from \\\"@mdx_components/integration_install_tooltip.mdx\\\";\\n\",\n    \"import Npm2Yarn from \\\"@theme/Npm2Yarn\\\";\\n\",\n    \"\\n\",\n    \"<IntegrationInstallTooltip></IntegrationInstallTooltip>\\n\",\n    \"\\n\",\n    \"<Npm2Yarn>\\n\",\n    \"  langchain\\n\",\n    \"</Npm2Yarn>\\n\",\n    \"```\\n\",\n    \"\\n\",\n    \"### Credentials\\n\",\n    \"\\n\",\n    \"If you want to get automated tracing of your model calls you can also set your [LangSmith](https://docs.smith.langchain.com/) API key by uncommenting below:\\n\",\n    \"\\n\",\n    \"```typescript\\n\",\n    \"// process.env.LANGCHAIN_TRACING_V2=\\\"true\\\"\\n\",\n    \"// process.env.LANGCHAIN_API_KEY=\\\"your-api-key\\\"\\n\",\n    \"```\"\n   ]\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"93df377e\",\n   \"metadata\": {},\n   \"source\": [\n    \"## Instantiation\\n\",\n    \"\\n\",\n    \"In this example we'll use OpenAIEmbeddings, however you can use any embeddings you like.\"\n   ]\n  },\n  {\n   \"cell_type\": \"code\",\n   \"execution_count\": 2,\n   \"id\": \"dc37144c-208d-4ab3-9f3a-0407a69fe052\",\n   \"metadata\": {\n    \"tags\": []\n   },\n   \"outputs\": [],\n   \"source\": [\n    \"import { MemoryVectorStore } from 'langchain/vectorstores/memory'\\n\",\n    \"import { OpenAIEmbeddings } from '@langchain/openai'\\n\",\n    \"\\n\",\n    \"const vectorStore = new MemoryVectorStore(new OpenAIEmbeddings())\"",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1705945143",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6414,
        "pr_file": "docs/core_docs/docs/integrations/vectorstores/memory.ipynb",
        "discussion_id": "1705945143",
        "commented_code": "@@ -0,0 +1,382 @@\n+{\n+ \"cells\": [\n+  {\n+   \"cell_type\": \"raw\",\n+   \"id\": \"1957f5cb\",\n+   \"metadata\": {\n+    \"vscode\": {\n+     \"languageId\": \"raw\"\n+    }\n+   },\n+   \"source\": [\n+    \"---\\n\",\n+    \"sidebar_label: In Memory\\n\",\n+    \"---\"\n+   ]\n+  },\n+  {\n+   \"cell_type\": \"markdown\",\n+   \"id\": \"ef1f0986\",\n+   \"metadata\": {},\n+   \"source\": [\n+    \"# MemoryVectorStore\\n\",\n+    \"\\n\",\n+    \"MemoryVectorStore is an in-memory, ephemeral vectorstore that stores embeddings in-memory and does an exact, linear search for the most similar embeddings. The default similarity metric is cosine similarity, but can be changed to any of the similarity metrics supported by [ml-distance](https://mljs.github.io/distance/modules/similarity.html).\\n\"\n+   ]\n+  },\n+  {\n+   \"cell_type\": \"markdown\",\n+   \"id\": \"36fdc060\",\n+   \"metadata\": {},\n+   \"source\": [\n+    \"## Setup\\n\",\n+    \"\\n\",\n+    \"To access the in memory vector store you'll need to install the `langchain` integration package.\\n\",\n+    \"\\n\",\n+    \"```{=mdx}\\n\",\n+    \"import IntegrationInstallTooltip from \\\"@mdx_components/integration_install_tooltip.mdx\\\";\\n\",\n+    \"import Npm2Yarn from \\\"@theme/Npm2Yarn\\\";\\n\",\n+    \"\\n\",\n+    \"<IntegrationInstallTooltip></IntegrationInstallTooltip>\\n\",\n+    \"\\n\",\n+    \"<Npm2Yarn>\\n\",\n+    \"  langchain\\n\",\n+    \"</Npm2Yarn>\\n\",\n+    \"```\\n\",\n+    \"\\n\",\n+    \"### Credentials\\n\",\n+    \"\\n\",\n+    \"If you want to get automated tracing of your model calls you can also set your [LangSmith](https://docs.smith.langchain.com/) API key by uncommenting below:\\n\",\n+    \"\\n\",\n+    \"```typescript\\n\",\n+    \"// process.env.LANGCHAIN_TRACING_V2=\\\"true\\\"\\n\",\n+    \"// process.env.LANGCHAIN_API_KEY=\\\"your-api-key\\\"\\n\",\n+    \"```\"\n+   ]\n+  },\n+  {\n+   \"cell_type\": \"markdown\",\n+   \"id\": \"93df377e\",\n+   \"metadata\": {},\n+   \"source\": [\n+    \"## Instantiation\\n\",\n+    \"\\n\",\n+    \"In this example we'll use OpenAIEmbeddings, however you can use any embeddings you like.\"\n+   ]\n+  },\n+  {\n+   \"cell_type\": \"code\",\n+   \"execution_count\": 2,\n+   \"id\": \"dc37144c-208d-4ab3-9f3a-0407a69fe052\",\n+   \"metadata\": {\n+    \"tags\": []\n+   },\n+   \"outputs\": [],\n+   \"source\": [\n+    \"import { MemoryVectorStore } from 'langchain/vectorstores/memory'\\n\",\n+    \"import { OpenAIEmbeddings } from '@langchain/openai'\\n\",\n+    \"\\n\",\n+    \"const vectorStore = new MemoryVectorStore(new OpenAIEmbeddings())\"",
        "comment_created_at": "2024-08-06T18:21:09+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "I would show how to initialize `.fromDocuments` as well as from an existing store",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1901243077",
    "pr_number": 7344,
    "pr_file": "docs/core_docs/docs/integrations/retrievers/azion-edgesql.mdx",
    "created_at": "2025-01-02T20:39:24+00:00",
    "commented_code": "### Azion Edge SQL Retriever",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1901243077",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7344,
        "pr_file": "docs/core_docs/docs/integrations/retrievers/azion-edgesql.mdx",
        "discussion_id": "1901243077",
        "commented_code": "@@ -0,0 +1,53 @@\n+### Azion Edge SQL Retriever",
        "comment_created_at": "2025-01-02T20:39:24+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Can we have this use the standard retriever template?\r\n\r\nhttps://github.com/langchain-ai/langchainjs/blob/main/libs/langchain-scripts/src/cli/docs/templates/retrievers.ipynb",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1908152475",
    "pr_number": 7450,
    "pr_file": "docs/core_docs/docs/integrations/text_embedding/bytedance_doubao.mdx",
    "created_at": "2025-01-09T04:32:02+00:00",
    "commented_code": null,
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1908152475",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7450,
        "pr_file": "docs/core_docs/docs/integrations/text_embedding/bytedance_doubao.mdx",
        "discussion_id": "1908152475",
        "commented_code": null,
        "comment_created_at": "2025-01-09T04:32:02+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Can you use the embeddings docs template?\r\n\r\nhttps://github.com/langchain-ai/langchainjs/blob/main/.github/contributing/INTEGRATIONS.md#documentation-and-integration-tests\r\nhttps://github.com/langchain-ai/langchainjs/blob/main/libs/langchain-scripts/src/cli/docs/templates/text_embedding.ipynb",
        "pr_file_module": null
      },
      {
        "comment_id": "1909012708",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7450,
        "pr_file": "docs/core_docs/docs/integrations/text_embedding/bytedance_doubao.mdx",
        "discussion_id": "1908152475",
        "commented_code": null,
        "comment_created_at": "2025-01-09T15:25:11+00:00",
        "comment_author": "ucev",
        "comment_body": "done. an exquisite design. i know how it works generally now.\ud83d\udc4d",
        "pr_file_module": null
      }
    ]
  }
]
