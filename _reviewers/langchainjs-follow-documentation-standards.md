---
title: Follow documentation standards
description: Ensure all documentation follows established templates and includes required
  sections. When referencing components, add links to their documentation pages. Documentation
  for each component type (like LLMs or vector stores) should follow its specific
  template format and include standard sections such as "Overview" with links to conceptual
  guides and...
repository: langchain-ai/langchainjs
label: Documentation
language: Other
comments_count: 5
repository_stars: 15004
---

Ensure all documentation follows established templates and includes required sections. When referencing components, add links to their documentation pages. Documentation for each component type (like LLMs or vector stores) should follow its specific template format and include standard sections such as "Overview" with links to conceptual guides and reference tables.

When a component is mentioned in documentation text, include a hyperlink to its own documentation:

```typescript
// Good example with proper cross-referencing
/**
 * The Semantic Cache feature leverages [AzureCosmosDBNoSQLVectorStore](/docs/integrations/vectorstores/azure_cosmosdb_nosql) 
 * which stores vector embeddings of cached prompts for similarity-based searches.
 * 
 * @see For more details, refer to the [Vector Store conceptual guide](/docs/concepts/vector_stores)
 */
```

Complete documentation should exist for all public APIs and referenced components. If documentation for a referenced component is missing (like `JsonOutputFunctionsParser`), create it before finalizing the referencing documentation.


[
  {
    "discussion_id": "1818683829",
    "pr_number": 7033,
    "pr_file": "docs/core_docs/docs/integrations/semantic_caches/azure_cosmosdb_nosql.mdx",
    "created_at": "2024-10-28T09:23:41+00:00",
    "commented_code": "# Azure Cosmos DB NoSQL Semantic Cache\n\n> The Semantic Cache feature is supported with Azure Cosmos DB for NoSQL integration, enabling users to retrieve cached responses based on semantic similarity between the user input and previously cached results. It leverages AzureCosmosDBNoSQLVectorStore, which stores vector embeddings of cached prompts. These embeddings enable similarity-based searches, allowing the system to retrieve relevant cached results.",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1818683829",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7033,
        "pr_file": "docs/core_docs/docs/integrations/semantic_caches/azure_cosmosdb_nosql.mdx",
        "discussion_id": "1818683829",
        "commented_code": "@@ -0,0 +1,40 @@\n+# Azure Cosmos DB NoSQL Semantic Cache\n+\n+> The Semantic Cache feature is supported with Azure Cosmos DB for NoSQL integration, enabling users to retrieve cached responses based on semantic similarity between the user input and previously cached results. It leverages AzureCosmosDBNoSQLVectorStore, which stores vector embeddings of cached prompts. These embeddings enable similarity-based searches, allowing the system to retrieve relevant cached results.",
        "comment_created_at": "2024-10-28T09:23:41+00:00",
        "comment_author": "sinedied",
        "comment_body": "nit: a link to AzureCosmosDBNoSQLVectorStore doc would be nice here",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1790893773",
    "pr_number": 6916,
    "pr_file": "docs/core_docs/docs/integrations/llms/ibm.mdx",
    "created_at": "2024-10-07T21:23:10+00:00",
    "commented_code": "# @langchain/community/llm/ibm",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1790893773",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6916,
        "pr_file": "docs/core_docs/docs/integrations/llms/ibm.mdx",
        "discussion_id": "1790893773",
        "commented_code": "@@ -0,0 +1,166 @@\n+# @langchain/community/llm/ibm",
        "comment_created_at": "2024-10-07T21:23:10+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Please make the docs pages follow this format:\r\n\r\nhttps://github.com/langchain-ai/langchainjs/blob/main/libs/langchain-scripts/src/cli/docs/templates/llms.ipynb",
        "pr_file_module": null
      },
      {
        "comment_id": "1792028645",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6916,
        "pr_file": "docs/core_docs/docs/integrations/llms/ibm.mdx",
        "discussion_id": "1790893773",
        "commented_code": "@@ -0,0 +1,166 @@\n+# @langchain/community/llm/ibm",
        "comment_created_at": "2024-10-08T14:48:40+00:00",
        "comment_author": "FilipZmijewski",
        "comment_body": "Done",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1788321017",
    "pr_number": 6904,
    "pr_file": "docs/core_docs/docs/integrations/vectorstores/libsql.mdx",
    "created_at": "2024-10-04T21:03:58+00:00",
    "commented_code": "# libSQL",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1788321017",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6904,
        "pr_file": "docs/core_docs/docs/integrations/vectorstores/libsql.mdx",
        "discussion_id": "1788321017",
        "commented_code": "@@ -0,0 +1,112 @@\n+# libSQL",
        "comment_created_at": "2024-10-04T21:03:58+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Can we make the docs follow this template?\r\n\r\nhttps://github.com/langchain-ai/langchainjs/blob/main/libs/langchain-scripts/src/cli/docs/templates/vectorstores.ipynb\r\n\r\nI need to update the contributing instructions...",
        "pr_file_module": null
      },
      {
        "comment_id": "1789964364",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6904,
        "pr_file": "docs/core_docs/docs/integrations/vectorstores/libsql.mdx",
        "discussion_id": "1788321017",
        "commented_code": "@@ -0,0 +1,112 @@\n+# libSQL",
        "comment_created_at": "2024-10-07T10:35:37+00:00",
        "comment_author": "notrab",
        "comment_body": "@jacoblee93 I updated the docs to follow more closely your example, however if you have time, please suggest or commit any changes you desire.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1375272196",
    "pr_number": 3065,
    "pr_file": "docs/docs/modules/chains/popular/structured_output.mdx",
    "created_at": "2023-10-28T15:33:49+00:00",
    "commented_code": "<CodeBlock language=\"typescript\">{FormatExample}</CodeBlock>\n\n# With chat history memory\n\nIn this example we'll construct a simple chain which uses OpenAI functions, structured output parser and chat history memory.\nWe'll provide the chain with two functions:\n\n- `food_recorder` -> A function to record what food a user likes.\n- `final_response` -> The function that returns a response to the user\n\nAfter each LLM response, we'll take our structured data and save it to memory (with a little formatting too). By doing this, we're enabling our LLM to\nremember what the user has said and use that information to generate a response.\n\nThe first step is to create our functions. For this we'll use `zod` to create the function schemas.\n\nWe're going to create two, one which returns an array of foods with their name, whether or not they're healthy and their color.\nThe second simply returns an object containing the final response.\n\n```typescript\nconst foodZodSchema = z.object({\n  foods: z\n    .array(\n      z.object({\n        name: z.string().describe(\"The name of the food item\"),\n        healthy: z.boolean().describe(\"Whether the food is good for you\"),\n        color: z.string().optional().describe(\"The color of the food\"),\n      })\n    )\n    .describe(\"An array of food items mentioned in the text\"),\n});\n\nconst finalResponseZodSchema = z.object({\n  finalResponse: z.string().describe(\"The final response\"),\n});\n```\n\nNext we'll construct the prompt. We have two \"messages\", one from the AI with a simple explanation on when to use the functions, and an input variable for the chat history. The second only contains the users question.\n\n```typescript\nconst prompt = ChatPromptTemplate.fromMessages([\n  [\n    \"ai\",\n    `You are a helpful assistant.\nYou are provided with two functions: one to use to record what food the user likes, and one to use when replying to user questions.\nChat history: {history}`,\n  ],\n  [\"human\", \"Question: {input}\"],\n]);\n```\n\nThen, define the LLM model and bind the function arguments to it. By using `.bind()` we're adding the functions to the model for every call.\n\nWe also must wrap our `zod` schemas with `zodToJsonSchema` to appropriately format them for OpenAI.\n\n```typescript\nconst model = new ChatOpenAI({\n  temperature: 0,\n}).bind({\n  functions: [\n    {\n      name: \"food_recorder\",\n      description: \"A function to record what food a user likes\",\n      parameters: zodToJsonSchema(foodZodSchema),\n    },\n    {\n      name: \"final_response\",\n      description: \"The function that returns a response to the user\",\n      parameters: zodToJsonSchema(finalResponseZodSchema),\n    },\n  ],\n});\n```\n\nNext we can define our memory using the `BufferMemory` class, and the output parser for structured data: `JsonOutputFunctionsParser`.",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1375272196",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3065,
        "pr_file": "docs/docs/modules/chains/popular/structured_output.mdx",
        "discussion_id": "1375272196",
        "commented_code": "@@ -34,6 +34,167 @@ import FormatExample from \"@examples/chains/openai_functions_structured_format.t\n \n <CodeBlock language=\"typescript\">{FormatExample}</CodeBlock>\n \n+# With chat history memory\n+\n+In this example we'll construct a simple chain which uses OpenAI functions, structured output parser and chat history memory.\n+We'll provide the chain with two functions:\n+\n+- `food_recorder` -> A function to record what food a user likes.\n+- `final_response` -> The function that returns a response to the user\n+\n+After each LLM response, we'll take our structured data and save it to memory (with a little formatting too). By doing this, we're enabling our LLM to\n+remember what the user has said and use that information to generate a response.\n+\n+The first step is to create our functions. For this we'll use `zod` to create the function schemas.\n+\n+We're going to create two, one which returns an array of foods with their name, whether or not they're healthy and their color.\n+The second simply returns an object containing the final response.\n+\n+```typescript\n+const foodZodSchema = z.object({\n+  foods: z\n+    .array(\n+      z.object({\n+        name: z.string().describe(\"The name of the food item\"),\n+        healthy: z.boolean().describe(\"Whether the food is good for you\"),\n+        color: z.string().optional().describe(\"The color of the food\"),\n+      })\n+    )\n+    .describe(\"An array of food items mentioned in the text\"),\n+});\n+\n+const finalResponseZodSchema = z.object({\n+  finalResponse: z.string().describe(\"The final response\"),\n+});\n+```\n+\n+Next we'll construct the prompt. We have two \"messages\", one from the AI with a simple explanation on when to use the functions, and an input variable for the chat history. The second only contains the users question.\n+\n+```typescript\n+const prompt = ChatPromptTemplate.fromMessages([\n+  [\n+    \"ai\",\n+    `You are a helpful assistant.\n+You are provided with two functions: one to use to record what food the user likes, and one to use when replying to user questions.\n+Chat history: {history}`,\n+  ],\n+  [\"human\", \"Question: {input}\"],\n+]);\n+```\n+\n+Then, define the LLM model and bind the function arguments to it. By using `.bind()` we're adding the functions to the model for every call.\n+\n+We also must wrap our `zod` schemas with `zodToJsonSchema` to appropriately format them for OpenAI.\n+\n+```typescript\n+const model = new ChatOpenAI({\n+  temperature: 0,\n+}).bind({\n+  functions: [\n+    {\n+      name: \"food_recorder\",\n+      description: \"A function to record what food a user likes\",\n+      parameters: zodToJsonSchema(foodZodSchema),\n+    },\n+    {\n+      name: \"final_response\",\n+      description: \"The function that returns a response to the user\",\n+      parameters: zodToJsonSchema(finalResponseZodSchema),\n+    },\n+  ],\n+});\n+```\n+\n+Next we can define our memory using the `BufferMemory` class, and the output parser for structured data: `JsonOutputFunctionsParser`.",
        "comment_created_at": "2023-10-28T15:33:49+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "We should definitely add docs for `JsonOutputFunctionsParser`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1705941918",
    "pr_number": 6414,
    "pr_file": "docs/core_docs/docs/integrations/vectorstores/memory.ipynb",
    "created_at": "2024-08-06T18:18:05+00:00",
    "commented_code": "{\n \"cells\": [\n  {\n   \"cell_type\": \"raw\",\n   \"id\": \"1957f5cb\",\n   \"metadata\": {\n    \"vscode\": {\n     \"languageId\": \"raw\"\n    }\n   },\n   \"source\": [\n    \"---\\n\",\n    \"sidebar_label: In Memory\\n\",\n    \"---\"\n   ]\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"ef1f0986\",\n   \"metadata\": {},\n   \"source\": [\n    \"# MemoryVectorStore\\n\",\n    \"\\n\",\n    \"MemoryVectorStore is an in-memory, ephemeral vectorstore that stores embeddings in-memory and does an exact, linear search for the most similar embeddings. The default similarity metric is cosine similarity, but can be changed to any of the similarity metrics supported by [ml-distance](https://mljs.github.io/distance/modules/similarity.html).\\n\"\n   ]",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1705941918",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6414,
        "pr_file": "docs/core_docs/docs/integrations/vectorstores/memory.ipynb",
        "discussion_id": "1705941918",
        "commented_code": "@@ -0,0 +1,382 @@\n+{\n+ \"cells\": [\n+  {\n+   \"cell_type\": \"raw\",\n+   \"id\": \"1957f5cb\",\n+   \"metadata\": {\n+    \"vscode\": {\n+     \"languageId\": \"raw\"\n+    }\n+   },\n+   \"source\": [\n+    \"---\\n\",\n+    \"sidebar_label: In Memory\\n\",\n+    \"---\"\n+   ]\n+  },\n+  {\n+   \"cell_type\": \"markdown\",\n+   \"id\": \"ef1f0986\",\n+   \"metadata\": {},\n+   \"source\": [\n+    \"# MemoryVectorStore\\n\",\n+    \"\\n\",\n+    \"MemoryVectorStore is an in-memory, ephemeral vectorstore that stores embeddings in-memory and does an exact, linear search for the most similar embeddings. The default similarity metric is cosine similarity, but can be changed to any of the similarity metrics supported by [ml-distance](https://mljs.github.io/distance/modules/similarity.html).\\n\"\n+   ]",
        "comment_created_at": "2024-08-06T18:18:05+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Should we have the `## Overview` boilerplate?",
        "pr_file_module": null
      },
      {
        "comment_id": "1705942925",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6414,
        "pr_file": "docs/core_docs/docs/integrations/vectorstores/memory.ipynb",
        "discussion_id": "1705941918",
        "commented_code": "@@ -0,0 +1,382 @@\n+{\n+ \"cells\": [\n+  {\n+   \"cell_type\": \"raw\",\n+   \"id\": \"1957f5cb\",\n+   \"metadata\": {\n+    \"vscode\": {\n+     \"languageId\": \"raw\"\n+    }\n+   },\n+   \"source\": [\n+    \"---\\n\",\n+    \"sidebar_label: In Memory\\n\",\n+    \"---\"\n+   ]\n+  },\n+  {\n+   \"cell_type\": \"markdown\",\n+   \"id\": \"ef1f0986\",\n+   \"metadata\": {},\n+   \"source\": [\n+    \"# MemoryVectorStore\\n\",\n+    \"\\n\",\n+    \"MemoryVectorStore is an in-memory, ephemeral vectorstore that stores embeddings in-memory and does an exact, linear search for the most similar embeddings. The default similarity metric is cosine similarity, but can be changed to any of the similarity metrics supported by [ml-distance](https://mljs.github.io/distance/modules/similarity.html).\\n\"\n+   ]",
        "comment_created_at": "2024-08-06T18:19:01+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Should at least link to vector store conceptual docs and details table",
        "pr_file_module": null
      }
    ]
  }
]
