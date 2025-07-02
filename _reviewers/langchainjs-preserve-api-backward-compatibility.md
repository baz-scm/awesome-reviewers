---
title: Preserve API backward compatibility
description: When modifying existing APIs, maintain backward compatibility by implementing
  changes in a non-breaking way. Use method overloading, optional parameters, or deprecation
  notices rather than direct breaking changes.
repository: langchain-ai/langchainjs
label: API
language: Typescript
comments_count: 7
repository_stars: 15004
---

When modifying existing APIs, maintain backward compatibility by implementing changes in a non-breaking way. Use method overloading, optional parameters, or deprecation notices rather than direct breaking changes.

Example of proper API evolution:

```typescript
// Instead of changing existing interface:
interface DeleteParams {
  ids: string[];
}

// Add overloaded method signatures:
class Store {
  // Original method
  async delete(ids: string[]): Promise<void>;
  // New overload with expanded functionality
  async delete(params: DeleteParams): Promise<void>;
  // Implementation handling both cases
  async delete(idsOrParams: string[] | DeleteParams): Promise<void> {
    if (Array.isArray(idsOrParams)) {
      // Handle legacy case
      return this.deleteByIds(idsOrParams);
    }
    // Handle new case
    return this.deleteWithParams(idsOrParams);
  }
}

// For deprecations, add clear notices:
/** @deprecated Use newMethod() instead. Will be removed in next major version. */
```

This approach allows gradual migration to new patterns while maintaining existing integrations. When deprecating functionality, provide clear migration paths and timeline in documentation.


[
  {
    "discussion_id": "1433346407",
    "pr_number": 3448,
    "pr_file": "langchain/src/chat_models/azure_ml.ts",
    "created_at": "2023-12-21T01:36:53+00:00",
    "commented_code": "import { SimpleChatModel, BaseChatModelParams } from \"./base.js\";\nimport { AzureMLHttpClient } from \"../llms/azure_ml.js\";\nimport { getEnvironmentVariable } from \"../util/env.js\";\nimport { BaseMessage } from \"../schema/index.js\";\n\nexport interface ChatContentFormatter {\n  /**\n   * Formats the request payload for the AzureML endpoint. It takes a\n   * prompt and a dictionary of model arguments as input and returns a\n   * string representing the formatted request payload.\n   * @param messages A list of messages for the chat so far.\n   * @param modelArgs A dictionary of model arguments.\n   * @returns A string representing the formatted request payload.\n   */\n  formatRequestPayload: (\n    messages: BaseMessage[],\n    modelArgs: Record<string, unknown>\n  ) => string;\n  /**\n   * Formats the response payload from the AzureML endpoint. It takes a\n   * response payload as input and returns a string representing the\n   * formatted response.\n   * @param responsePayload The response payload from the AzureML endpoint.\n   * @returns A string representing the formatted response.\n   */\n  formatResponsePayload: (output: string) => string;\n}\n\nexport class LlamaContentFormatter implements ChatContentFormatter {\n  _convertMessageToRecord(message: BaseMessage): Record<string, unknown> {\n    if (message._getType() === \"human\") {\n      return { role: \"user\", content: message.content };\n    } else if (message._getType() === \"ai\") {\n      return { role: \"assistant\", content: message.content };\n    } else {\n      return { role: message._getType(), content: message.content };\n    }\n  }\n\n  formatRequestPayload(\n    messages: BaseMessage[],\n    modelArgs: Record<string, unknown>\n  ): string {\n    let msgs = messages.map((message) => {\n      this._convertMessageToRecord(message);\n    });\n    return JSON.stringify({\n      input_data: {\n        input_string: msgs,\n        parameters: modelArgs,\n      },\n    });\n  }\n\n  formatResponsePayload(responsePayload: string) {\n    const response = JSON.parse(responsePayload);\n    return response.output;\n  }\n}\n\n/**\n * Type definition for the input parameters of the AzureMLChatOnlineEndpoint class.\n */\nexport interface AzureMLChatParams extends BaseChatModelParams {\n  endpointUrl?: string;\n  endpointApiKey?: string;\n  modelArgs?: Record<string, unknown>;\n  contentFormatter?: ChatContentFormatter;\n}\n\n/**\n * Class that represents the chat model. It extends the SimpleChatModel class and implements the AzureMLChatInput interface.\n */\nexport class AzureMLChatOnlineEndpoint\n  extends SimpleChatModel\n  implements AzureMLChatParams\n{\n  static lc_name() {\n    return \"AzureMLChatOnlineEndpoint\";\n  }\n  static lc_description() {\n    return \"A class for interacting with AzureML Chat models.\";\n  }\n  endpointUrl: string;\n  endpointApiKey: string;\n  modelArgs?: Record<string, unknown>;\n  contentFormatter: ChatContentFormatter;\n  httpClient: AzureMLHttpClient;\n\n  constructor(fields: AzureMLChatParams) {\n    super(fields ?? {});\n    if (!fields?.endpointUrl && !getEnvironmentVariable(\"AZUREML_URL\")) {\n      throw new Error(\"No Azure ML Url found.\");\n    }\n    if (!fields?.endpointApiKey && !getEnvironmentVariable(\"AZUREML_API_KEY\")) {\n      throw new Error(\"No Azure ML ApiKey found.\");\n    }\n    if (!fields?.contentFormatter) {\n      throw new Error(\"No Content Formatter provided.\");",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1433346407",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3448,
        "pr_file": "langchain/src/chat_models/azure_ml.ts",
        "discussion_id": "1433346407",
        "commented_code": "@@ -0,0 +1,142 @@\n+import { SimpleChatModel, BaseChatModelParams } from \"./base.js\";\n+import { AzureMLHttpClient } from \"../llms/azure_ml.js\";\n+import { getEnvironmentVariable } from \"../util/env.js\";\n+import { BaseMessage } from \"../schema/index.js\";\n+\n+export interface ChatContentFormatter {\n+  /**\n+   * Formats the request payload for the AzureML endpoint. It takes a\n+   * prompt and a dictionary of model arguments as input and returns a\n+   * string representing the formatted request payload.\n+   * @param messages A list of messages for the chat so far.\n+   * @param modelArgs A dictionary of model arguments.\n+   * @returns A string representing the formatted request payload.\n+   */\n+  formatRequestPayload: (\n+    messages: BaseMessage[],\n+    modelArgs: Record<string, unknown>\n+  ) => string;\n+  /**\n+   * Formats the response payload from the AzureML endpoint. It takes a\n+   * response payload as input and returns a string representing the\n+   * formatted response.\n+   * @param responsePayload The response payload from the AzureML endpoint.\n+   * @returns A string representing the formatted response.\n+   */\n+  formatResponsePayload: (output: string) => string;\n+}\n+\n+export class LlamaContentFormatter implements ChatContentFormatter {\n+  _convertMessageToRecord(message: BaseMessage): Record<string, unknown> {\n+    if (message._getType() === \"human\") {\n+      return { role: \"user\", content: message.content };\n+    } else if (message._getType() === \"ai\") {\n+      return { role: \"assistant\", content: message.content };\n+    } else {\n+      return { role: message._getType(), content: message.content };\n+    }\n+  }\n+\n+  formatRequestPayload(\n+    messages: BaseMessage[],\n+    modelArgs: Record<string, unknown>\n+  ): string {\n+    let msgs = messages.map((message) => {\n+      this._convertMessageToRecord(message);\n+    });\n+    return JSON.stringify({\n+      input_data: {\n+        input_string: msgs,\n+        parameters: modelArgs,\n+      },\n+    });\n+  }\n+\n+  formatResponsePayload(responsePayload: string) {\n+    const response = JSON.parse(responsePayload);\n+    return response.output;\n+  }\n+}\n+\n+/**\n+ * Type definition for the input parameters of the AzureMLChatOnlineEndpoint class.\n+ */\n+export interface AzureMLChatParams extends BaseChatModelParams {\n+  endpointUrl?: string;\n+  endpointApiKey?: string;\n+  modelArgs?: Record<string, unknown>;\n+  contentFormatter?: ChatContentFormatter;\n+}\n+\n+/**\n+ * Class that represents the chat model. It extends the SimpleChatModel class and implements the AzureMLChatInput interface.\n+ */\n+export class AzureMLChatOnlineEndpoint\n+  extends SimpleChatModel\n+  implements AzureMLChatParams\n+{\n+  static lc_name() {\n+    return \"AzureMLChatOnlineEndpoint\";\n+  }\n+  static lc_description() {\n+    return \"A class for interacting with AzureML Chat models.\";\n+  }\n+  endpointUrl: string;\n+  endpointApiKey: string;\n+  modelArgs?: Record<string, unknown>;\n+  contentFormatter: ChatContentFormatter;\n+  httpClient: AzureMLHttpClient;\n+\n+  constructor(fields: AzureMLChatParams) {\n+    super(fields ?? {});\n+    if (!fields?.endpointUrl && !getEnvironmentVariable(\"AZUREML_URL\")) {\n+      throw new Error(\"No Azure ML Url found.\");\n+    }\n+    if (!fields?.endpointApiKey && !getEnvironmentVariable(\"AZUREML_API_KEY\")) {\n+      throw new Error(\"No Azure ML ApiKey found.\");\n+    }\n+    if (!fields?.contentFormatter) {\n+      throw new Error(\"No Content Formatter provided.\");",
        "comment_created_at": "2023-12-21T01:36:53+00:00",
        "comment_author": "bracesproul",
        "comment_body": "Instead of this check it should be a required param in the `AzureMLChatParams` interface. But why are we requiring users to pass this in? Can we instead keep it optional and have a default formatter that gets used?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2057154690",
    "pr_number": 8056,
    "pr_file": "libs/langchain-aws/src/tests/chat_models.int.test.ts",
    "created_at": "2025-04-24T01:17:37+00:00",
    "commented_code": "expect(typeof result.tool_calls![0].args.location).toBe(\"string\");\n  expect(result.tool_calls![0].args.location.length).toBeGreaterThan(0);\n\n  messages.push(\n    new ToolMessage({\n      tool_call_id: result.tool_calls![0].id!,\n      content: await tools[0].invoke(result.tool_calls![0]),\n    })\n  );\n  messages.push(await tools[0].invoke(result.tool_calls![0]));",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2057154690",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8056,
        "pr_file": "libs/langchain-aws/src/tests/chat_models.int.test.ts",
        "discussion_id": "2057154690",
        "commented_code": "@@ -513,12 +513,7 @@ test(\"Test ChatBedrockConverse can respond to tool invocations with thinking ena\n   expect(typeof result.tool_calls![0].args.location).toBe(\"string\");\n   expect(result.tool_calls![0].args.location.length).toBeGreaterThan(0);\n \n-  messages.push(\n-    new ToolMessage({\n-      tool_call_id: result.tool_calls![0].id!,\n-      content: await tools[0].invoke(result.tool_calls![0]),\n-    })\n-  );\n+  messages.push(await tools[0].invoke(result.tool_calls![0]));",
        "comment_created_at": "2025-04-24T01:17:37+00:00",
        "comment_author": "hntrl",
        "comment_body": "StructuredTool.invoke will return a tool message when a tool call is passed, so we don't have to create a new tool message here",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1424769745",
    "pr_number": 3577,
    "pr_file": "libs/langchain-community/src/llms/watsonx_ai.ts",
    "created_at": "2023-12-13T02:13:17+00:00",
    "commented_code": "};\n  }\n\n  endpoint: string;\n\n  region = \"us-south\";\n\n  version = \"2023-05-29\";\n\n  modelId = \"meta-llama/llama-2-70b-chat\";\n\n  modelKwargs?: Record<string, unknown>;\n\n  ibmCloudApiKey?: string;\n\n  ibmCloudToken?: string;\n  projectId!: string;\n\n  ibmCloudTokenExpiresAt?: number;\n  modelParameters?: WatsonModelParameters;\n\n  projectId?: string;\n\n  modelParameters?: Record<string, unknown>;\n  private readonly watsonApiClient: WatsonApiClient;\n\n  constructor(fields: WatsonxAIParams) {\n    super(fields);\n\n    this.region = fields?.region ?? this.region;",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1424769745",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3577,
        "pr_file": "libs/langchain-community/src/llms/watsonx_ai.ts",
        "discussion_id": "1424769745",
        "commented_code": "@@ -69,48 +30,43 @@ export class WatsonxAI extends LLM<BaseLLMCallOptions> {\n     };\n   }\n \n-  endpoint: string;\n-\n-  region = \"us-south\";\n-\n-  version = \"2023-05-29\";\n-\n   modelId = \"meta-llama/llama-2-70b-chat\";\n \n   modelKwargs?: Record<string, unknown>;\n \n-  ibmCloudApiKey?: string;\n-\n-  ibmCloudToken?: string;\n+  projectId!: string;\n \n-  ibmCloudTokenExpiresAt?: number;\n+  modelParameters?: WatsonModelParameters;\n \n-  projectId?: string;\n-\n-  modelParameters?: Record<string, unknown>;\n+  private readonly watsonApiClient: WatsonApiClient;\n \n   constructor(fields: WatsonxAIParams) {\n     super(fields);\n \n-    this.region = fields?.region ?? this.region;",
        "comment_created_at": "2023-12-13T02:13:17+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Isn't removing all of these a breaking change?",
        "pr_file_module": null
      },
      {
        "comment_id": "1424977554",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3577,
        "pr_file": "libs/langchain-community/src/llms/watsonx_ai.ts",
        "discussion_id": "1424769745",
        "commented_code": "@@ -69,48 +30,43 @@ export class WatsonxAI extends LLM<BaseLLMCallOptions> {\n     };\n   }\n \n-  endpoint: string;\n-\n-  region = \"us-south\";\n-\n-  version = \"2023-05-29\";\n-\n   modelId = \"meta-llama/llama-2-70b-chat\";\n \n   modelKwargs?: Record<string, unknown>;\n \n-  ibmCloudApiKey?: string;\n-\n-  ibmCloudToken?: string;\n+  projectId!: string;\n \n-  ibmCloudTokenExpiresAt?: number;\n+  modelParameters?: WatsonModelParameters;\n \n-  projectId?: string;\n-\n-  modelParameters?: Record<string, unknown>;\n+  private readonly watsonApiClient: WatsonApiClient;\n \n   constructor(fields: WatsonxAIParams) {\n     super(fields);\n \n-    this.region = fields?.region ?? this.region;",
        "comment_created_at": "2023-12-13T08:00:44+00:00",
        "comment_author": "faileon",
        "comment_body": "I moved a few attributes to the WatsonClient as it's something I also needed in the ChatModel. I did remove `lc_serializable = true;` by accident and will add it back in.\r\n\r\nI tried running the provided example at `examples/src/llms/watsonx_ai.ts` and it works like before.",
        "pr_file_module": null
      },
      {
        "comment_id": "1425542720",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3577,
        "pr_file": "libs/langchain-community/src/llms/watsonx_ai.ts",
        "discussion_id": "1424769745",
        "commented_code": "@@ -69,48 +30,43 @@ export class WatsonxAI extends LLM<BaseLLMCallOptions> {\n     };\n   }\n \n-  endpoint: string;\n-\n-  region = \"us-south\";\n-\n-  version = \"2023-05-29\";\n-\n   modelId = \"meta-llama/llama-2-70b-chat\";\n \n   modelKwargs?: Record<string, unknown>;\n \n-  ibmCloudApiKey?: string;\n-\n-  ibmCloudToken?: string;\n+  projectId!: string;\n \n-  ibmCloudTokenExpiresAt?: number;\n+  modelParameters?: WatsonModelParameters;\n \n-  projectId?: string;\n-\n-  modelParameters?: Record<string, unknown>;\n+  private readonly watsonApiClient: WatsonApiClient;\n \n   constructor(fields: WatsonxAIParams) {\n     super(fields);\n \n-    this.region = fields?.region ?? this.region;",
        "comment_created_at": "2023-12-13T15:44:14+00:00",
        "comment_author": "chasemcdo",
        "comment_body": "It is breaking in the sense that if someone is dependent on the old schema they'll need to update it, but most of the functionality is there, but in a now more reusable format.\r\n\r\nOne thing that I am noticing missing is there was originally an [endpoint](https://github.com/langchain-ai/langchainjs/blob/06a39117aae61fcbf26a537de4bad8a156bbb9ab/libs/langchain-community/src/llms/watsonx_ai.ts#L14-L17) parameter which would allow the end user to overwrite the entire url if they so desired.\r\n\r\nI had included this since the production endpoint is still labeled as \"beta\", so this would allow someone to migrate to a different (potentially more stable) endpoint as soon as it is released without the need to submit a PR to LangChain.\r\n\r\nThoughts on reintroducing that @faileon ?",
        "pr_file_module": null
      },
      {
        "comment_id": "1425755461",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3577,
        "pr_file": "libs/langchain-community/src/llms/watsonx_ai.ts",
        "discussion_id": "1424769745",
        "commented_code": "@@ -69,48 +30,43 @@ export class WatsonxAI extends LLM<BaseLLMCallOptions> {\n     };\n   }\n \n-  endpoint: string;\n-\n-  region = \"us-south\";\n-\n-  version = \"2023-05-29\";\n-\n   modelId = \"meta-llama/llama-2-70b-chat\";\n \n   modelKwargs?: Record<string, unknown>;\n \n-  ibmCloudApiKey?: string;\n-\n-  ibmCloudToken?: string;\n+  projectId!: string;\n \n-  ibmCloudTokenExpiresAt?: number;\n+  modelParameters?: WatsonModelParameters;\n \n-  projectId?: string;\n-\n-  modelParameters?: Record<string, unknown>;\n+  private readonly watsonApiClient: WatsonApiClient;\n \n   constructor(fields: WatsonxAIParams) {\n     super(fields);\n \n-    this.region = fields?.region ?? this.region;",
        "comment_created_at": "2023-12-13T18:48:59+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Not sure what current usage is, but would love a shim for principle's sake. I can try to have a look later if you don't have time.",
        "pr_file_module": null
      },
      {
        "comment_id": "1426735975",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3577,
        "pr_file": "libs/langchain-community/src/llms/watsonx_ai.ts",
        "discussion_id": "1424769745",
        "commented_code": "@@ -69,48 +30,43 @@ export class WatsonxAI extends LLM<BaseLLMCallOptions> {\n     };\n   }\n \n-  endpoint: string;\n-\n-  region = \"us-south\";\n-\n-  version = \"2023-05-29\";\n-\n   modelId = \"meta-llama/llama-2-70b-chat\";\n \n   modelKwargs?: Record<string, unknown>;\n \n-  ibmCloudApiKey?: string;\n-\n-  ibmCloudToken?: string;\n+  projectId!: string;\n \n-  ibmCloudTokenExpiresAt?: number;\n+  modelParameters?: WatsonModelParameters;\n \n-  projectId?: string;\n-\n-  modelParameters?: Record<string, unknown>;\n+  private readonly watsonApiClient: WatsonApiClient;\n \n   constructor(fields: WatsonxAIParams) {\n     super(fields);\n \n-    this.region = fields?.region ?? this.region;",
        "comment_created_at": "2023-12-14T13:42:44+00:00",
        "comment_author": "faileon",
        "comment_body": "Ah I get it now, yes this would be breaking to someone using the old schema. I can revert it and make it backwards compatible.\r\n\r\nRegarding the endpoint parameter that's a good catch, I agree it should be configurable, as it will most likely change once IBM releases non beta version.\r\n\r\nI have some free time during this weekend again to work on it.",
        "pr_file_module": null
      },
      {
        "comment_id": "1427152346",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3577,
        "pr_file": "libs/langchain-community/src/llms/watsonx_ai.ts",
        "discussion_id": "1424769745",
        "commented_code": "@@ -69,48 +30,43 @@ export class WatsonxAI extends LLM<BaseLLMCallOptions> {\n     };\n   }\n \n-  endpoint: string;\n-\n-  region = \"us-south\";\n-\n-  version = \"2023-05-29\";\n-\n   modelId = \"meta-llama/llama-2-70b-chat\";\n \n   modelKwargs?: Record<string, unknown>;\n \n-  ibmCloudApiKey?: string;\n-\n-  ibmCloudToken?: string;\n+  projectId!: string;\n \n-  ibmCloudTokenExpiresAt?: number;\n+  modelParameters?: WatsonModelParameters;\n \n-  projectId?: string;\n-\n-  modelParameters?: Record<string, unknown>;\n+  private readonly watsonApiClient: WatsonApiClient;\n \n   constructor(fields: WatsonxAIParams) {\n     super(fields);\n \n-    this.region = fields?.region ?? this.region;",
        "comment_created_at": "2023-12-14T19:01:09+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Thank you! This is a very recent integration, but we really try to not have any breaking changes in patches unless they are completely unavoidable.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2048025111",
    "pr_number": 8020,
    "pr_file": "langchain-core/src/messages/index.ts",
    "created_at": "2025-04-17T01:04:27+00:00",
    "commented_code": "type InvalidToolCall,\n  isToolMessage,\n  isToolMessageChunk,\n  type ToolCall,",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2048025111",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8020,
        "pr_file": "langchain-core/src/messages/index.ts",
        "discussion_id": "2048025111",
        "commented_code": "@@ -16,4 +16,5 @@ export {\n   type InvalidToolCall,\n   isToolMessage,\n   isToolMessageChunk,\n+  type ToolCall,",
        "comment_created_at": "2025-04-17T01:04:27+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "This conflicts with the `ToolCall` declared in `base.ts` - you should import it like this:\r\n\r\n```ts\r\nimport { type ToolCall } from \"@langchain/core/messages/tool\";\r\n```\r\n\r\nWe will remove the old type on next breaking change.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1708007834",
    "pr_number": 6133,
    "pr_file": "libs/langchain-azure-cosmosdb/src/azure_cosmosdb_mongodb.ts",
    "created_at": "2024-08-07T22:15:25+00:00",
    "commented_code": "import {\n  ObjectId,\n  Collection,\n  Document as MongoDBDocument,\n  MongoClient,\n  Db,\n  Filter,\n} from \"mongodb\";\nimport type { EmbeddingsInterface } from \"@langchain/core/embeddings\";\nimport {\n  MaxMarginalRelevanceSearchOptions,\n  VectorStore,\n} from \"@langchain/core/vectorstores\";\nimport { Document, DocumentInterface } from \"@langchain/core/documents\";\nimport { maximalMarginalRelevance } from \"@langchain/core/utils/math\";\nimport { getEnvironmentVariable } from \"@langchain/core/utils/env\";\n\n/** Azure Cosmos DB for MongoDB vCore Similarity type. */\nexport const AzureCosmosDBMongoDBSimilarityType = {\n  /** Cosine similarity */\n  COS: \"COS\",\n  /** Inner - product */\n  IP: \"IP\",\n  /** Euclidian distance */\n  L2: \"L2\",\n} as const;\n\n/** Azure Cosmos DB for MongoDB vCore Similarity type. */\nexport type AzureCosmosDBMongoDBSimilarityType =\n  (typeof AzureCosmosDBMongoDBSimilarityType)[keyof typeof AzureCosmosDBMongoDBSimilarityType];\n\n/** Azure Cosmos DB for MongoDB vCore Index Options. */\nexport type AzureCosmosDBMongoDBIndexOptions = {\n  /** Skips automatic index creation. */\n  readonly skipCreate?: boolean;\n  /** Number of clusters that the inverted file (IVF) index uses to group the vector data. */\n  readonly numLists?: number;\n  /** Number of dimensions for vector similarity. */\n  readonly dimensions?: number;\n  /** Similarity metric to use with the IVF index. */\n  readonly similarity?: AzureCosmosDBMongoDBSimilarityType;\n};\n\n/** Azure Cosmos DB for MongoDB vCore delete Parameters. */\nexport type AzureCosmosDBMongoDBDeleteParams = {\n  /** List of IDs for the documents to be removed. */\n  readonly ids?: string | string[];\n  /** MongoDB filter object or list of IDs for the documents to be removed. */\n  readonly filter?: Filter<MongoDBDocument>;\n};\n\n/** Configuration options for the `AzureCosmosDBMongoDBVectorStore` constructor. */\nexport interface AzureCosmosDBMongoDBConfig {\n  readonly client?: MongoClient;\n  readonly connectionString?: string;\n  readonly databaseName?: string;\n  readonly collectionName?: string;\n  readonly indexName?: string;\n  readonly textKey?: string;\n  readonly embeddingKey?: string;\n  readonly indexOptions?: AzureCosmosDBMongoDBIndexOptions;\n}\n\n/**\n * Azure Cosmos DB for MongoDB vCore vector store.\n * To use this, you should have both:\n * - the `mongodb` NPM package installed\n * - a connection string associated with a MongoDB VCore Cluster\n *\n * You do not need to create a database or collection, it will be created\n * automatically.\n *\n * You also need an index on the collection, which is by default be created\n * automatically using the `createIndex` method.\n */\nexport class AzureCosmosDBMongoDBVectorStore extends VectorStore {\n  get lc_secrets(): { [key: string]: string } {\n    return {\n      connectionString: \"AZURE_COSMOSDB_MONGODB_CONNECTION_STRING\",\n    };\n  }\n\n  private connectPromise: Promise<void>;\n\n  private initPromise: Promise<void>;\n\n  private readonly client: MongoClient | undefined;\n\n  private database: Db;\n\n  private collection: Collection<MongoDBDocument>;\n\n  readonly indexName: string;\n\n  readonly textKey: string;\n\n  readonly embeddingKey: string;\n\n  private readonly indexOptions: AzureCosmosDBMongoDBIndexOptions;\n\n  /**\n   * Initializes the AzureCosmosDBMongoDBVectorStore.\n   * Connect the client to the database and create the container, creating them if needed.\n   * @returns A promise that resolves when the AzureCosmosDBMongoDBVectorStore has been initialized.\n   */\n  initialize: () => Promise<void>;\n\n  _vectorstoreType(): string {\n    return \"azure_cosmosdb_mongodb\";\n  }\n\n  constructor(\n    embeddings: EmbeddingsInterface,\n    dbConfig: AzureCosmosDBMongoDBConfig\n  ) {\n    super(embeddings, dbConfig);\n\n    const connectionString =\n      dbConfig.connectionString ??\n      getEnvironmentVariable(\"AZURE_COSMOSDB_MONGODB_CONNECTION_STRING\");\n\n    if (!dbConfig.client && !connectionString) {\n      throw new Error(\n        \"AzureCosmosDBMongoDBVectorStore client or connection string must be set.\"\n      );\n    }\n\n    if (!dbConfig.client) {\n      // eslint-disable-next-line @typescript-eslint/no-non-null-assertion\n      this.client = new MongoClient(connectionString!, {\n        appName: \"langchainjs\",\n      });\n    }\n\n    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion\n    const client = dbConfig.client || this.client!;\n    const databaseName = dbConfig.databaseName ?? \"documentsDB\";\n    const collectionName = dbConfig.collectionName ?? \"documents\";\n    this.indexName = dbConfig.indexName ?? \"vectorSearchIndex\";\n    this.textKey = dbConfig.textKey ?? \"textContent\";\n    this.embeddingKey = dbConfig.embeddingKey ?? \"vectorContent\";\n    this.indexOptions = dbConfig.indexOptions ?? {};\n\n    // Deferring initialization to the first call to `initialize`\n    this.initialize = () => {",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1708007834",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6133,
        "pr_file": "libs/langchain-azure-cosmosdb/src/azure_cosmosdb_mongodb.ts",
        "discussion_id": "1708007834",
        "commented_code": "@@ -0,0 +1,496 @@\n+import {\n+  ObjectId,\n+  Collection,\n+  Document as MongoDBDocument,\n+  MongoClient,\n+  Db,\n+  Filter,\n+} from \"mongodb\";\n+import type { EmbeddingsInterface } from \"@langchain/core/embeddings\";\n+import {\n+  MaxMarginalRelevanceSearchOptions,\n+  VectorStore,\n+} from \"@langchain/core/vectorstores\";\n+import { Document, DocumentInterface } from \"@langchain/core/documents\";\n+import { maximalMarginalRelevance } from \"@langchain/core/utils/math\";\n+import { getEnvironmentVariable } from \"@langchain/core/utils/env\";\n+\n+/** Azure Cosmos DB for MongoDB vCore Similarity type. */\n+export const AzureCosmosDBMongoDBSimilarityType = {\n+  /** Cosine similarity */\n+  COS: \"COS\",\n+  /** Inner - product */\n+  IP: \"IP\",\n+  /** Euclidian distance */\n+  L2: \"L2\",\n+} as const;\n+\n+/** Azure Cosmos DB for MongoDB vCore Similarity type. */\n+export type AzureCosmosDBMongoDBSimilarityType =\n+  (typeof AzureCosmosDBMongoDBSimilarityType)[keyof typeof AzureCosmosDBMongoDBSimilarityType];\n+\n+/** Azure Cosmos DB for MongoDB vCore Index Options. */\n+export type AzureCosmosDBMongoDBIndexOptions = {\n+  /** Skips automatic index creation. */\n+  readonly skipCreate?: boolean;\n+  /** Number of clusters that the inverted file (IVF) index uses to group the vector data. */\n+  readonly numLists?: number;\n+  /** Number of dimensions for vector similarity. */\n+  readonly dimensions?: number;\n+  /** Similarity metric to use with the IVF index. */\n+  readonly similarity?: AzureCosmosDBMongoDBSimilarityType;\n+};\n+\n+/** Azure Cosmos DB for MongoDB vCore delete Parameters. */\n+export type AzureCosmosDBMongoDBDeleteParams = {\n+  /** List of IDs for the documents to be removed. */\n+  readonly ids?: string | string[];\n+  /** MongoDB filter object or list of IDs for the documents to be removed. */\n+  readonly filter?: Filter<MongoDBDocument>;\n+};\n+\n+/** Configuration options for the `AzureCosmosDBMongoDBVectorStore` constructor. */\n+export interface AzureCosmosDBMongoDBConfig {\n+  readonly client?: MongoClient;\n+  readonly connectionString?: string;\n+  readonly databaseName?: string;\n+  readonly collectionName?: string;\n+  readonly indexName?: string;\n+  readonly textKey?: string;\n+  readonly embeddingKey?: string;\n+  readonly indexOptions?: AzureCosmosDBMongoDBIndexOptions;\n+}\n+\n+/**\n+ * Azure Cosmos DB for MongoDB vCore vector store.\n+ * To use this, you should have both:\n+ * - the `mongodb` NPM package installed\n+ * - a connection string associated with a MongoDB VCore Cluster\n+ *\n+ * You do not need to create a database or collection, it will be created\n+ * automatically.\n+ *\n+ * You also need an index on the collection, which is by default be created\n+ * automatically using the `createIndex` method.\n+ */\n+export class AzureCosmosDBMongoDBVectorStore extends VectorStore {\n+  get lc_secrets(): { [key: string]: string } {\n+    return {\n+      connectionString: \"AZURE_COSMOSDB_MONGODB_CONNECTION_STRING\",\n+    };\n+  }\n+\n+  private connectPromise: Promise<void>;\n+\n+  private initPromise: Promise<void>;\n+\n+  private readonly client: MongoClient | undefined;\n+\n+  private database: Db;\n+\n+  private collection: Collection<MongoDBDocument>;\n+\n+  readonly indexName: string;\n+\n+  readonly textKey: string;\n+\n+  readonly embeddingKey: string;\n+\n+  private readonly indexOptions: AzureCosmosDBMongoDBIndexOptions;\n+\n+  /**\n+   * Initializes the AzureCosmosDBMongoDBVectorStore.\n+   * Connect the client to the database and create the container, creating them if needed.\n+   * @returns A promise that resolves when the AzureCosmosDBMongoDBVectorStore has been initialized.\n+   */\n+  initialize: () => Promise<void>;\n+\n+  _vectorstoreType(): string {\n+    return \"azure_cosmosdb_mongodb\";\n+  }\n+\n+  constructor(\n+    embeddings: EmbeddingsInterface,\n+    dbConfig: AzureCosmosDBMongoDBConfig\n+  ) {\n+    super(embeddings, dbConfig);\n+\n+    const connectionString =\n+      dbConfig.connectionString ??\n+      getEnvironmentVariable(\"AZURE_COSMOSDB_MONGODB_CONNECTION_STRING\");\n+\n+    if (!dbConfig.client && !connectionString) {\n+      throw new Error(\n+        \"AzureCosmosDBMongoDBVectorStore client or connection string must be set.\"\n+      );\n+    }\n+\n+    if (!dbConfig.client) {\n+      // eslint-disable-next-line @typescript-eslint/no-non-null-assertion\n+      this.client = new MongoClient(connectionString!, {\n+        appName: \"langchainjs\",\n+      });\n+    }\n+\n+    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion\n+    const client = dbConfig.client || this.client!;\n+    const databaseName = dbConfig.databaseName ?? \"documentsDB\";\n+    const collectionName = dbConfig.collectionName ?? \"documents\";\n+    this.indexName = dbConfig.indexName ?? \"vectorSearchIndex\";\n+    this.textKey = dbConfig.textKey ?? \"textContent\";\n+    this.embeddingKey = dbConfig.embeddingKey ?? \"vectorContent\";\n+    this.indexOptions = dbConfig.indexOptions ?? {};\n+\n+    // Deferring initialization to the first call to `initialize`\n+    this.initialize = () => {",
        "comment_created_at": "2024-08-07T22:15:25+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Would prefer this as a static method like this:\r\n\r\nhttps://v02.api.js.langchain.com/classes/langchain_community_vectorstores_pgvector.PGVectorStore.html#initialize\r\n\r\nSince I'm not sure this will show up well in API refs, but won't block on it",
        "pr_file_module": null
      },
      {
        "comment_id": "1708897351",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6133,
        "pr_file": "libs/langchain-azure-cosmosdb/src/azure_cosmosdb_mongodb.ts",
        "discussion_id": "1708007834",
        "commented_code": "@@ -0,0 +1,496 @@\n+import {\n+  ObjectId,\n+  Collection,\n+  Document as MongoDBDocument,\n+  MongoClient,\n+  Db,\n+  Filter,\n+} from \"mongodb\";\n+import type { EmbeddingsInterface } from \"@langchain/core/embeddings\";\n+import {\n+  MaxMarginalRelevanceSearchOptions,\n+  VectorStore,\n+} from \"@langchain/core/vectorstores\";\n+import { Document, DocumentInterface } from \"@langchain/core/documents\";\n+import { maximalMarginalRelevance } from \"@langchain/core/utils/math\";\n+import { getEnvironmentVariable } from \"@langchain/core/utils/env\";\n+\n+/** Azure Cosmos DB for MongoDB vCore Similarity type. */\n+export const AzureCosmosDBMongoDBSimilarityType = {\n+  /** Cosine similarity */\n+  COS: \"COS\",\n+  /** Inner - product */\n+  IP: \"IP\",\n+  /** Euclidian distance */\n+  L2: \"L2\",\n+} as const;\n+\n+/** Azure Cosmos DB for MongoDB vCore Similarity type. */\n+export type AzureCosmosDBMongoDBSimilarityType =\n+  (typeof AzureCosmosDBMongoDBSimilarityType)[keyof typeof AzureCosmosDBMongoDBSimilarityType];\n+\n+/** Azure Cosmos DB for MongoDB vCore Index Options. */\n+export type AzureCosmosDBMongoDBIndexOptions = {\n+  /** Skips automatic index creation. */\n+  readonly skipCreate?: boolean;\n+  /** Number of clusters that the inverted file (IVF) index uses to group the vector data. */\n+  readonly numLists?: number;\n+  /** Number of dimensions for vector similarity. */\n+  readonly dimensions?: number;\n+  /** Similarity metric to use with the IVF index. */\n+  readonly similarity?: AzureCosmosDBMongoDBSimilarityType;\n+};\n+\n+/** Azure Cosmos DB for MongoDB vCore delete Parameters. */\n+export type AzureCosmosDBMongoDBDeleteParams = {\n+  /** List of IDs for the documents to be removed. */\n+  readonly ids?: string | string[];\n+  /** MongoDB filter object or list of IDs for the documents to be removed. */\n+  readonly filter?: Filter<MongoDBDocument>;\n+};\n+\n+/** Configuration options for the `AzureCosmosDBMongoDBVectorStore` constructor. */\n+export interface AzureCosmosDBMongoDBConfig {\n+  readonly client?: MongoClient;\n+  readonly connectionString?: string;\n+  readonly databaseName?: string;\n+  readonly collectionName?: string;\n+  readonly indexName?: string;\n+  readonly textKey?: string;\n+  readonly embeddingKey?: string;\n+  readonly indexOptions?: AzureCosmosDBMongoDBIndexOptions;\n+}\n+\n+/**\n+ * Azure Cosmos DB for MongoDB vCore vector store.\n+ * To use this, you should have both:\n+ * - the `mongodb` NPM package installed\n+ * - a connection string associated with a MongoDB VCore Cluster\n+ *\n+ * You do not need to create a database or collection, it will be created\n+ * automatically.\n+ *\n+ * You also need an index on the collection, which is by default be created\n+ * automatically using the `createIndex` method.\n+ */\n+export class AzureCosmosDBMongoDBVectorStore extends VectorStore {\n+  get lc_secrets(): { [key: string]: string } {\n+    return {\n+      connectionString: \"AZURE_COSMOSDB_MONGODB_CONNECTION_STRING\",\n+    };\n+  }\n+\n+  private connectPromise: Promise<void>;\n+\n+  private initPromise: Promise<void>;\n+\n+  private readonly client: MongoClient | undefined;\n+\n+  private database: Db;\n+\n+  private collection: Collection<MongoDBDocument>;\n+\n+  readonly indexName: string;\n+\n+  readonly textKey: string;\n+\n+  readonly embeddingKey: string;\n+\n+  private readonly indexOptions: AzureCosmosDBMongoDBIndexOptions;\n+\n+  /**\n+   * Initializes the AzureCosmosDBMongoDBVectorStore.\n+   * Connect the client to the database and create the container, creating them if needed.\n+   * @returns A promise that resolves when the AzureCosmosDBMongoDBVectorStore has been initialized.\n+   */\n+  initialize: () => Promise<void>;\n+\n+  _vectorstoreType(): string {\n+    return \"azure_cosmosdb_mongodb\";\n+  }\n+\n+  constructor(\n+    embeddings: EmbeddingsInterface,\n+    dbConfig: AzureCosmosDBMongoDBConfig\n+  ) {\n+    super(embeddings, dbConfig);\n+\n+    const connectionString =\n+      dbConfig.connectionString ??\n+      getEnvironmentVariable(\"AZURE_COSMOSDB_MONGODB_CONNECTION_STRING\");\n+\n+    if (!dbConfig.client && !connectionString) {\n+      throw new Error(\n+        \"AzureCosmosDBMongoDBVectorStore client or connection string must be set.\"\n+      );\n+    }\n+\n+    if (!dbConfig.client) {\n+      // eslint-disable-next-line @typescript-eslint/no-non-null-assertion\n+      this.client = new MongoClient(connectionString!, {\n+        appName: \"langchainjs\",\n+      });\n+    }\n+\n+    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion\n+    const client = dbConfig.client || this.client!;\n+    const databaseName = dbConfig.databaseName ?? \"documentsDB\";\n+    const collectionName = dbConfig.collectionName ?? \"documents\";\n+    this.indexName = dbConfig.indexName ?? \"vectorSearchIndex\";\n+    this.textKey = dbConfig.textKey ?? \"textContent\";\n+    this.embeddingKey = dbConfig.embeddingKey ?? \"vectorContent\";\n+    this.indexOptions = dbConfig.indexOptions ?? {};\n+\n+    // Deferring initialization to the first call to `initialize`\n+    this.initialize = () => {",
        "comment_created_at": "2024-08-08T08:04:50+00:00",
        "comment_author": "sinedied",
        "comment_body": "Would you be ok with a middle ground approach?\r\n- make the current `initialize` method I made internal\r\n- add a new static `initialize` method the calls constructor + init/connect the db connection\r\n- keep the \"automatic\" init when calling any VS method in case it wasn't done before (for compatibility / simplicity)\r\n- explain how the init works in the docs\r\n\r\nMy reasoning: I'd like to make the migration from the previous implementation painless (ie keep the auto init) and also make it work for folks who skim quickly through docs and just call the constructor without using the `initialize` method",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1581599504",
    "pr_number": 5197,
    "pr_file": "libs/langchain-community/src/vectorstores/azure_cosmosdb.ts",
    "created_at": "2024-04-26T23:02:14+00:00",
    "commented_code": "/**\n   * Removes specified documents from the AzureCosmosDBVectorStore.\n   * @param ids IDs of the documents to be removed. If no IDs are specified,\n   *     all documents will be removed.\n   * If no IDs or filter are specified, all documents will be removed.\n   * @param ids A list of IDs for the documents to be removed.\n   * @param filter A MongoDB filter object or list of IDs for the documents to be removed.\n   * @returns A promise that resolves when the documents have been removed.\n   */\n  async delete(ids?: string[]): Promise<void> {\n  async delete(\n    ids?: string | string[],",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1581599504",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5197,
        "pr_file": "libs/langchain-community/src/vectorstores/azure_cosmosdb.ts",
        "discussion_id": "1581599504",
        "commented_code": "@@ -205,19 +233,27 @@ export class AzureCosmosDBVectorStore extends VectorStore {\n \n   /**\n    * Removes specified documents from the AzureCosmosDBVectorStore.\n-   * @param ids IDs of the documents to be removed. If no IDs are specified,\n-   *     all documents will be removed.\n+   * If no IDs or filter are specified, all documents will be removed.\n+   * @param ids A list of IDs for the documents to be removed.\n+   * @param filter A MongoDB filter object or list of IDs for the documents to be removed.\n    * @returns A promise that resolves when the documents have been removed.\n    */\n-  async delete(ids?: string[]): Promise<void> {\n+  async delete(\n+    ids?: string | string[],",
        "comment_created_at": "2024-04-26T23:02:14+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Hey sorry, no I mean a single param like this so as not to break the interface:\r\n\r\nhttps://github.com/langchain-ai/langchainjs/blob/main/libs/langchain-community/src/vectorstores/pinecone.ts#L174",
        "pr_file_module": null
      },
      {
        "comment_id": "1583227571",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5197,
        "pr_file": "libs/langchain-community/src/vectorstores/azure_cosmosdb.ts",
        "discussion_id": "1581599504",
        "commented_code": "@@ -205,19 +233,27 @@ export class AzureCosmosDBVectorStore extends VectorStore {\n \n   /**\n    * Removes specified documents from the AzureCosmosDBVectorStore.\n-   * @param ids IDs of the documents to be removed. If no IDs are specified,\n-   *     all documents will be removed.\n+   * If no IDs or filter are specified, all documents will be removed.\n+   * @param ids A list of IDs for the documents to be removed.\n+   * @param filter A MongoDB filter object or list of IDs for the documents to be removed.\n    * @returns A promise that resolves when the documents have been removed.\n    */\n-  async delete(ids?: string[]): Promise<void> {\n+  async delete(\n+    ids?: string | string[],",
        "comment_created_at": "2024-04-29T14:55:22+00:00",
        "comment_author": "sinedied",
        "comment_body": "Done, I updated and rebased the PR",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1583971678",
    "pr_number": 5197,
    "pr_file": "libs/langchain-community/src/vectorstores/azure_cosmosdb.ts",
    "created_at": "2024-04-30T00:17:08+00:00",
    "commented_code": "/**\n   * Removes specified documents from the AzureCosmosDBVectorStore.\n   * @param ids IDs of the documents to be removed. If no IDs are specified,\n   *     all documents will be removed.\n   * If no IDs or filter are specified, all documents will be removed.\n   * @param params Parameters for the delete operation.\n   * @returns A promise that resolves when the documents have been removed.\n   */\n  async delete(ids?: string[]): Promise<void> {\n  async delete(params: AzureCosmosDBDeleteParams = {}): Promise<void> {",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1583971678",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5197,
        "pr_file": "libs/langchain-community/src/vectorstores/azure_cosmosdb.ts",
        "discussion_id": "1583971678",
        "commented_code": "@@ -205,19 +241,24 @@ export class AzureCosmosDBVectorStore extends VectorStore {\n \n   /**\n    * Removes specified documents from the AzureCosmosDBVectorStore.\n-   * @param ids IDs of the documents to be removed. If no IDs are specified,\n-   *     all documents will be removed.\n+   * If no IDs or filter are specified, all documents will be removed.\n+   * @param params Parameters for the delete operation.\n    * @returns A promise that resolves when the documents have been removed.\n    */\n-  async delete(ids?: string[]): Promise<void> {\n+  async delete(params: AzureCosmosDBDeleteParams = {}): Promise<void> {",
        "comment_created_at": "2024-04-30T00:17:08+00:00",
        "comment_author": "bracesproul",
        "comment_body": "This will be a breaking change. Instead we should overload this func so both input types are allowed, and we can narrow the type inside of the method.",
        "pr_file_module": null
      }
    ]
  }
]
