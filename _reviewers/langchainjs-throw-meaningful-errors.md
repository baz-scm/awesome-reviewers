---
title: Throw meaningful errors
description: Always throw specific, actionable errors instead of returning unexpected
  values or simply logging issues. Error messages should be clear, concise, and contain
  the exact reason for failure without redundancy.
repository: langchain-ai/langchainjs
label: Error Handling
language: Typescript
comments_count: 5
repository_stars: 15004
---

Always throw specific, actionable errors instead of returning unexpected values or simply logging issues. Error messages should be clear, concise, and contain the exact reason for failure without redundancy.

Consider these practices:

1. When a function can't perform its task, throw an error rather than returning a default value:
```typescript
// Bad
_combineLLMOutput(): Record<string, any> | undefined {
  return [];  // Returns unexpected empty array
}

// Good
_combineLLMOutput(): Record<string, any> | undefined {
  throw new Error("AzureMLChatOnlineEndpoint._combineLLMOutput called, but is not implemented.");
}
```

2. Avoid redundant error prefixes that will be repeated in logs:
```typescript
// Bad - creates redundant messages
if (!response.ok) {
  throw new Error(`Error authenticating with Reddit: ${response.statusText}`);
}

// Good - concise and clear
if (!response.ok) {
  throw new Error(response.statusText);
}
```

3. Propagate errors instead of just logging them to allow proper handling up the call stack:
```typescript
// Bad - swallows the error
try {
  await this.collection.deleteMany({});
} catch (error) {
  console.log("Error clearing sessions:", error);
}

// Good - allows callers to handle the error
try {
  await this.collection.deleteMany({});
} catch (error) {
  console.error("Error clearing sessions:", error);
  throw error; // Re-throw or throw a more specific error
}
```

4. Preserve error structures expected by error handling mechanisms:
```typescript
// Bad - overwrites properties needed for retry logic
(error as any).details = { /* ... */ };

// Good - maintains expected structure
(error as any).response = res;
```

Well-designed error handling improves debugging efficiency and creates a more robust application.


[
  {
    "discussion_id": "1899693765",
    "pr_number": 7300,
    "pr_file": "libs/langchain-community/src/utils/reddit.ts",
    "created_at": "2024-12-30T17:32:20+00:00",
    "commented_code": "import dotenv from \"dotenv\";\nimport { AsyncCaller } from \"@langchain/core/utils/async_caller\";\n\ndotenv.config();\n\nexport interface RedditAPIConfig {\n  clientId: string;\n  clientSecret: string;\n  userAgent: string;\n}\n\nexport interface RedditPost {\n  title: string;\n  selftext: string;\n  subreddit_name_prefixed: string;\n  score: number;\n  id: string;\n  url: string;\n  author: string;\n}\n\nexport class RedditAPIWrapper {\n  private clientId: string;\n\n  private clientSecret: string;\n\n  private userAgent: string;\n\n  private token: string | null = null;\n\n  private baseUrl = \"https://oauth.reddit.com\";\n\n  private asyncCaller: AsyncCaller; // Using AsyncCaller for requests\n\n  constructor(config: RedditAPIConfig) {\n    this.clientId = config.clientId;\n    this.clientSecret = config.clientSecret;\n    this.userAgent = config.userAgent;\n    this.asyncCaller = new AsyncCaller({\n      maxConcurrency: 5,\n      maxRetries: 3,\n      onFailedAttempt: (error) => {\n        console.error(\"Attempt failed:\", error.message);\n      },\n    });\n  }\n\n  private async authenticate() {\n    if (this.token) return;\n\n    const authString = btoa(`${this.clientId}:${this.clientSecret}`);\n\n    try {\n      const response = await fetch(\n        \"https://www.reddit.com/api/v1/access_token\",\n        {\n          method: \"POST\",\n          headers: {\n            Authorization: `Basic ${authString}`,\n            \"User-Agent\": this.userAgent,\n            \"Content-Type\": \"application/x-www-form-urlencoded\",\n          },\n          body: \"grant_type=client_credentials\",\n        }\n      );\n\n      if (!response.ok) {\n        throw new Error(\n          `Error authenticating with Reddit: ${response.statusText}`\n        );\n      }\n\n      const data = await response.json();\n      this.token = data.access_token;\n    } catch (error) {\n      console.error(\"Error authenticating with Reddit:\", error);\n    }",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1899693765",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7300,
        "pr_file": "libs/langchain-community/src/utils/reddit.ts",
        "discussion_id": "1899693765",
        "commented_code": "@@ -0,0 +1,145 @@\n+import dotenv from \"dotenv\";\n+import { AsyncCaller } from \"@langchain/core/utils/async_caller\";\n+\n+dotenv.config();\n+\n+export interface RedditAPIConfig {\n+  clientId: string;\n+  clientSecret: string;\n+  userAgent: string;\n+}\n+\n+export interface RedditPost {\n+  title: string;\n+  selftext: string;\n+  subreddit_name_prefixed: string;\n+  score: number;\n+  id: string;\n+  url: string;\n+  author: string;\n+}\n+\n+export class RedditAPIWrapper {\n+  private clientId: string;\n+\n+  private clientSecret: string;\n+\n+  private userAgent: string;\n+\n+  private token: string | null = null;\n+\n+  private baseUrl = \"https://oauth.reddit.com\";\n+\n+  private asyncCaller: AsyncCaller; // Using AsyncCaller for requests\n+\n+  constructor(config: RedditAPIConfig) {\n+    this.clientId = config.clientId;\n+    this.clientSecret = config.clientSecret;\n+    this.userAgent = config.userAgent;\n+    this.asyncCaller = new AsyncCaller({\n+      maxConcurrency: 5,\n+      maxRetries: 3,\n+      onFailedAttempt: (error) => {\n+        console.error(\"Attempt failed:\", error.message);\n+      },\n+    });\n+  }\n+\n+  private async authenticate() {\n+    if (this.token) return;\n+\n+    const authString = btoa(`${this.clientId}:${this.clientSecret}`);\n+\n+    try {\n+      const response = await fetch(\n+        \"https://www.reddit.com/api/v1/access_token\",\n+        {\n+          method: \"POST\",\n+          headers: {\n+            Authorization: `Basic ${authString}`,\n+            \"User-Agent\": this.userAgent,\n+            \"Content-Type\": \"application/x-www-form-urlencoded\",\n+          },\n+          body: \"grant_type=client_credentials\",\n+        }\n+      );\n+\n+      if (!response.ok) {\n+        throw new Error(\n+          `Error authenticating with Reddit: ${response.statusText}`\n+        );\n+      }\n+\n+      const data = await response.json();\n+      this.token = data.access_token;\n+    } catch (error) {\n+      console.error(\"Error authenticating with Reddit:\", error);\n+    }",
        "comment_created_at": "2024-12-30T17:32:20+00:00",
        "comment_author": "nick-w-nick",
        "comment_body": "If I am reading this correctly, if it encounters an issue, it will throw an error with the text \r\n\r\n`Error authenticating with Reddit: ${response.statusText}`\r\n\r\nbut will then do `console.error(\"Error authenticating with Reddit:\", error);`, which will output something like:\r\n```\r\nError authenticating with Reddit:\r\n  Error authenticating with Reddit: \"invalid auth token\"\r\n```\r\n\r\nI'd suggest just throwing the status text from Reddit instead and then logging out the authentication error in the catch instead.\r\n\r\n```suggestion\r\n      if (!response.ok) {\r\n        throw new Error(response.statusText);\r\n      }\r\n\r\n      const data = await response.json();\r\n      this.token = data.access_token;\r\n    } catch (error) {\r\n      console.error(\"Error authenticating with Reddit:\", error);\r\n    }\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1433348408",
    "pr_number": 3448,
    "pr_file": "langchain/src/chat_models/azure_ml.ts",
    "created_at": "2023-12-21T01:39:37+00:00",
    "commented_code": "import { SimpleChatModel, BaseChatModelParams } from \"./base.js\";\nimport { AzureMLHttpClient } from \"../llms/azure_ml.js\";\nimport { getEnvironmentVariable } from \"../util/env.js\";\nimport { BaseMessage } from \"../schema/index.js\";\n\nexport interface ChatContentFormatter {\n  /**\n   * Formats the request payload for the AzureML endpoint. It takes a\n   * prompt and a dictionary of model arguments as input and returns a\n   * string representing the formatted request payload.\n   * @param messages A list of messages for the chat so far.\n   * @param modelArgs A dictionary of model arguments.\n   * @returns A string representing the formatted request payload.\n   */\n  formatRequestPayload: (\n    messages: BaseMessage[],\n    modelArgs: Record<string, unknown>\n  ) => string;\n  /**\n   * Formats the response payload from the AzureML endpoint. It takes a\n   * response payload as input and returns a string representing the\n   * formatted response.\n   * @param responsePayload The response payload from the AzureML endpoint.\n   * @returns A string representing the formatted response.\n   */\n  formatResponsePayload: (output: string) => string;\n}\n\nexport class LlamaContentFormatter implements ChatContentFormatter {\n  _convertMessageToRecord(message: BaseMessage): Record<string, unknown> {\n    if (message._getType() === \"human\") {\n      return { role: \"user\", content: message.content };\n    } else if (message._getType() === \"ai\") {\n      return { role: \"assistant\", content: message.content };\n    } else {\n      return { role: message._getType(), content: message.content };\n    }\n  }\n\n  formatRequestPayload(\n    messages: BaseMessage[],\n    modelArgs: Record<string, unknown>\n  ): string {\n    let msgs = messages.map((message) => {\n      this._convertMessageToRecord(message);\n    });\n    return JSON.stringify({\n      input_data: {\n        input_string: msgs,\n        parameters: modelArgs,\n      },\n    });\n  }\n\n  formatResponsePayload(responsePayload: string) {\n    const response = JSON.parse(responsePayload);\n    return response.output;\n  }\n}\n\n/**\n * Type definition for the input parameters of the AzureMLChatOnlineEndpoint class.\n */\nexport interface AzureMLChatParams extends BaseChatModelParams {\n  endpointUrl?: string;\n  endpointApiKey?: string;\n  modelArgs?: Record<string, unknown>;\n  contentFormatter?: ChatContentFormatter;\n}\n\n/**\n * Class that represents the chat model. It extends the SimpleChatModel class and implements the AzureMLChatInput interface.\n */\nexport class AzureMLChatOnlineEndpoint\n  extends SimpleChatModel\n  implements AzureMLChatParams\n{\n  static lc_name() {\n    return \"AzureMLChatOnlineEndpoint\";\n  }\n  static lc_description() {\n    return \"A class for interacting with AzureML Chat models.\";\n  }\n  endpointUrl: string;\n  endpointApiKey: string;\n  modelArgs?: Record<string, unknown>;\n  contentFormatter: ChatContentFormatter;\n  httpClient: AzureMLHttpClient;\n\n  constructor(fields: AzureMLChatParams) {\n    super(fields ?? {});\n    if (!fields?.endpointUrl && !getEnvironmentVariable(\"AZUREML_URL\")) {\n      throw new Error(\"No Azure ML Url found.\");\n    }\n    if (!fields?.endpointApiKey && !getEnvironmentVariable(\"AZUREML_API_KEY\")) {\n      throw new Error(\"No Azure ML ApiKey found.\");\n    }\n    if (!fields?.contentFormatter) {\n      throw new Error(\"No Content Formatter provided.\");\n    }\n\n    this.endpointUrl =\n      fields.endpointUrl || getEnvironmentVariable(\"AZUREML_URL\") + \"\";\n    this.endpointApiKey =\n      fields.endpointApiKey || getEnvironmentVariable(\"AZUREML_API_KEY\") + \"\";\n    this.httpClient = new AzureMLHttpClient(\n      this.endpointUrl,\n      this.endpointApiKey\n    );\n    this.contentFormatter = fields.contentFormatter;\n    this.modelArgs = fields?.modelArgs;\n  }\n  get _identifying_params() {\n    const modelKwargs = this.modelArgs || {};\n    return {\n      ...super._identifyingParams,\n      modelKwargs,\n    };\n  }\n\n  _llmType() {\n    return \"azureml_chat\";\n  }\n\n  _combineLLMOutput(): Record<string, any> | undefined {\n    return [];",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1433348408",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3448,
        "pr_file": "langchain/src/chat_models/azure_ml.ts",
        "discussion_id": "1433348408",
        "commented_code": "@@ -0,0 +1,142 @@\n+import { SimpleChatModel, BaseChatModelParams } from \"./base.js\";\n+import { AzureMLHttpClient } from \"../llms/azure_ml.js\";\n+import { getEnvironmentVariable } from \"../util/env.js\";\n+import { BaseMessage } from \"../schema/index.js\";\n+\n+export interface ChatContentFormatter {\n+  /**\n+   * Formats the request payload for the AzureML endpoint. It takes a\n+   * prompt and a dictionary of model arguments as input and returns a\n+   * string representing the formatted request payload.\n+   * @param messages A list of messages for the chat so far.\n+   * @param modelArgs A dictionary of model arguments.\n+   * @returns A string representing the formatted request payload.\n+   */\n+  formatRequestPayload: (\n+    messages: BaseMessage[],\n+    modelArgs: Record<string, unknown>\n+  ) => string;\n+  /**\n+   * Formats the response payload from the AzureML endpoint. It takes a\n+   * response payload as input and returns a string representing the\n+   * formatted response.\n+   * @param responsePayload The response payload from the AzureML endpoint.\n+   * @returns A string representing the formatted response.\n+   */\n+  formatResponsePayload: (output: string) => string;\n+}\n+\n+export class LlamaContentFormatter implements ChatContentFormatter {\n+  _convertMessageToRecord(message: BaseMessage): Record<string, unknown> {\n+    if (message._getType() === \"human\") {\n+      return { role: \"user\", content: message.content };\n+    } else if (message._getType() === \"ai\") {\n+      return { role: \"assistant\", content: message.content };\n+    } else {\n+      return { role: message._getType(), content: message.content };\n+    }\n+  }\n+\n+  formatRequestPayload(\n+    messages: BaseMessage[],\n+    modelArgs: Record<string, unknown>\n+  ): string {\n+    let msgs = messages.map((message) => {\n+      this._convertMessageToRecord(message);\n+    });\n+    return JSON.stringify({\n+      input_data: {\n+        input_string: msgs,\n+        parameters: modelArgs,\n+      },\n+    });\n+  }\n+\n+  formatResponsePayload(responsePayload: string) {\n+    const response = JSON.parse(responsePayload);\n+    return response.output;\n+  }\n+}\n+\n+/**\n+ * Type definition for the input parameters of the AzureMLChatOnlineEndpoint class.\n+ */\n+export interface AzureMLChatParams extends BaseChatModelParams {\n+  endpointUrl?: string;\n+  endpointApiKey?: string;\n+  modelArgs?: Record<string, unknown>;\n+  contentFormatter?: ChatContentFormatter;\n+}\n+\n+/**\n+ * Class that represents the chat model. It extends the SimpleChatModel class and implements the AzureMLChatInput interface.\n+ */\n+export class AzureMLChatOnlineEndpoint\n+  extends SimpleChatModel\n+  implements AzureMLChatParams\n+{\n+  static lc_name() {\n+    return \"AzureMLChatOnlineEndpoint\";\n+  }\n+  static lc_description() {\n+    return \"A class for interacting with AzureML Chat models.\";\n+  }\n+  endpointUrl: string;\n+  endpointApiKey: string;\n+  modelArgs?: Record<string, unknown>;\n+  contentFormatter: ChatContentFormatter;\n+  httpClient: AzureMLHttpClient;\n+\n+  constructor(fields: AzureMLChatParams) {\n+    super(fields ?? {});\n+    if (!fields?.endpointUrl && !getEnvironmentVariable(\"AZUREML_URL\")) {\n+      throw new Error(\"No Azure ML Url found.\");\n+    }\n+    if (!fields?.endpointApiKey && !getEnvironmentVariable(\"AZUREML_API_KEY\")) {\n+      throw new Error(\"No Azure ML ApiKey found.\");\n+    }\n+    if (!fields?.contentFormatter) {\n+      throw new Error(\"No Content Formatter provided.\");\n+    }\n+\n+    this.endpointUrl =\n+      fields.endpointUrl || getEnvironmentVariable(\"AZUREML_URL\") + \"\";\n+    this.endpointApiKey =\n+      fields.endpointApiKey || getEnvironmentVariable(\"AZUREML_API_KEY\") + \"\";\n+    this.httpClient = new AzureMLHttpClient(\n+      this.endpointUrl,\n+      this.endpointApiKey\n+    );\n+    this.contentFormatter = fields.contentFormatter;\n+    this.modelArgs = fields?.modelArgs;\n+  }\n+  get _identifying_params() {\n+    const modelKwargs = this.modelArgs || {};\n+    return {\n+      ...super._identifyingParams,\n+      modelKwargs,\n+    };\n+  }\n+\n+  _llmType() {\n+    return \"azureml_chat\";\n+  }\n+\n+  _combineLLMOutput(): Record<string, any> | undefined {\n+    return [];",
        "comment_created_at": "2023-12-21T01:39:37+00:00",
        "comment_author": "bracesproul",
        "comment_body": "If it's not implemented, it should throw a not implemented error.\r\n```suggestion\r\n    throw new Error(\"AzureMLChatOnlineEndpoint._combineLLMOutput called, but is not implemented.\")\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1901634206",
    "pr_number": 7436,
    "pr_file": "libs/langchain-azure-cosmosdb/src/chat_histories/mongodb.ts",
    "created_at": "2025-01-03T10:04:10+00:00",
    "commented_code": "await this.collection.deleteOne({ [ID_KEY]: this.sessionId });\n  }\n\n  async getAllSessions(): Promise<ChatSession[]> {\n    await this.initialize();\n    const documents = await this.collection.find().toArray();\n\n    const chatSessions: ChatSession[] = documents.map((doc) => ({\n      id: doc[ID_KEY],\n      context: doc.context || {},\n    }));\n\n    return chatSessions;\n  }\n\n  async clearAllSessions() {\n    await this.initialize();\n    try {\n      await this.collection.deleteMany({});\n    } catch (error) {\n      console.log(\"Error clearing sessions:\", error);\n    }\n  }\n\n  async getContext(): Promise<Record<string, unknown>> {\n    await this.initialize();\n\n    const document = await this.collection.findOne({\n      [ID_KEY]: this.sessionId,\n    });\n    this.context = document?.context || this.context;\n    return this.context;\n  }\n\n  async setContext(context: Record<string, unknown>): Promise<void> {\n    await this.initialize();\n\n    try {\n      await this.collection.updateOne(\n        { [ID_KEY]: this.sessionId },\n        {\n          $set: { context },\n        },\n        { upsert: true }\n      );\n    } catch (error) {\n      console.log(\"Error setting context\", error);",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1901634206",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7436,
        "pr_file": "libs/langchain-azure-cosmosdb/src/chat_histories/mongodb.ts",
        "discussion_id": "1901634206",
        "commented_code": "@@ -152,4 +161,51 @@ export class AzureCosmosDBMongoChatMessageHistory extends BaseListChatMessageHis\n \n     await this.collection.deleteOne({ [ID_KEY]: this.sessionId });\n   }\n+\n+  async getAllSessions(): Promise<ChatSession[]> {\n+    await this.initialize();\n+    const documents = await this.collection.find().toArray();\n+\n+    const chatSessions: ChatSession[] = documents.map((doc) => ({\n+      id: doc[ID_KEY],\n+      context: doc.context || {},\n+    }));\n+\n+    return chatSessions;\n+  }\n+\n+  async clearAllSessions() {\n+    await this.initialize();\n+    try {\n+      await this.collection.deleteMany({});\n+    } catch (error) {\n+      console.log(\"Error clearing sessions:\", error);\n+    }\n+  }\n+\n+  async getContext(): Promise<Record<string, unknown>> {\n+    await this.initialize();\n+\n+    const document = await this.collection.findOne({\n+      [ID_KEY]: this.sessionId,\n+    });\n+    this.context = document?.context || this.context;\n+    return this.context;\n+  }\n+\n+  async setContext(context: Record<string, unknown>): Promise<void> {\n+    await this.initialize();\n+\n+    try {\n+      await this.collection.updateOne(\n+        { [ID_KEY]: this.sessionId },\n+        {\n+          $set: { context },\n+        },\n+        { upsert: true }\n+      );\n+    } catch (error) {\n+      console.log(\"Error setting context\", error);",
        "comment_created_at": "2025-01-03T10:04:10+00:00",
        "comment_author": "sinedied",
        "comment_body": "Would be better to throw so these errors can be identified",
        "pr_file_module": null
      },
      {
        "comment_id": "1912473317",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7436,
        "pr_file": "libs/langchain-azure-cosmosdb/src/chat_histories/mongodb.ts",
        "discussion_id": "1901634206",
        "commented_code": "@@ -152,4 +161,51 @@ export class AzureCosmosDBMongoChatMessageHistory extends BaseListChatMessageHis\n \n     await this.collection.deleteOne({ [ID_KEY]: this.sessionId });\n   }\n+\n+  async getAllSessions(): Promise<ChatSession[]> {\n+    await this.initialize();\n+    const documents = await this.collection.find().toArray();\n+\n+    const chatSessions: ChatSession[] = documents.map((doc) => ({\n+      id: doc[ID_KEY],\n+      context: doc.context || {},\n+    }));\n+\n+    return chatSessions;\n+  }\n+\n+  async clearAllSessions() {\n+    await this.initialize();\n+    try {\n+      await this.collection.deleteMany({});\n+    } catch (error) {\n+      console.log(\"Error clearing sessions:\", error);\n+    }\n+  }\n+\n+  async getContext(): Promise<Record<string, unknown>> {\n+    await this.initialize();\n+\n+    const document = await this.collection.findOne({\n+      [ID_KEY]: this.sessionId,\n+    });\n+    this.context = document?.context || this.context;\n+    return this.context;\n+  }\n+\n+  async setContext(context: Record<string, unknown>): Promise<void> {\n+    await this.initialize();\n+\n+    try {\n+      await this.collection.updateOne(\n+        { [ID_KEY]: this.sessionId },\n+        {\n+          $set: { context },\n+        },\n+        { upsert: true }\n+      );\n+    } catch (error) {\n+      console.log(\"Error setting context\", error);",
        "comment_created_at": "2025-01-12T15:12:16+00:00",
        "comment_author": "crisjy",
        "comment_body": "throw errors for this",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1901634285",
    "pr_number": 7436,
    "pr_file": "libs/langchain-azure-cosmosdb/src/chat_histories/mongodb.ts",
    "created_at": "2025-01-03T10:04:15+00:00",
    "commented_code": "await this.collection.deleteOne({ [ID_KEY]: this.sessionId });\n  }\n\n  async getAllSessions(): Promise<ChatSession[]> {\n    await this.initialize();\n    const documents = await this.collection.find().toArray();\n\n    const chatSessions: ChatSession[] = documents.map((doc) => ({\n      id: doc[ID_KEY],\n      context: doc.context || {},\n    }));\n\n    return chatSessions;\n  }\n\n  async clearAllSessions() {\n    await this.initialize();\n    try {\n      await this.collection.deleteMany({});\n    } catch (error) {\n      console.log(\"Error clearing sessions:\", error);",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1901634285",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7436,
        "pr_file": "libs/langchain-azure-cosmosdb/src/chat_histories/mongodb.ts",
        "discussion_id": "1901634285",
        "commented_code": "@@ -152,4 +161,51 @@ export class AzureCosmosDBMongoChatMessageHistory extends BaseListChatMessageHis\n \n     await this.collection.deleteOne({ [ID_KEY]: this.sessionId });\n   }\n+\n+  async getAllSessions(): Promise<ChatSession[]> {\n+    await this.initialize();\n+    const documents = await this.collection.find().toArray();\n+\n+    const chatSessions: ChatSession[] = documents.map((doc) => ({\n+      id: doc[ID_KEY],\n+      context: doc.context || {},\n+    }));\n+\n+    return chatSessions;\n+  }\n+\n+  async clearAllSessions() {\n+    await this.initialize();\n+    try {\n+      await this.collection.deleteMany({});\n+    } catch (error) {\n+      console.log(\"Error clearing sessions:\", error);",
        "comment_created_at": "2025-01-03T10:04:15+00:00",
        "comment_author": "sinedied",
        "comment_body": "Would be better to throw so these errors can be identified",
        "pr_file_module": null
      },
      {
        "comment_id": "1912473333",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7436,
        "pr_file": "libs/langchain-azure-cosmosdb/src/chat_histories/mongodb.ts",
        "discussion_id": "1901634285",
        "commented_code": "@@ -152,4 +161,51 @@ export class AzureCosmosDBMongoChatMessageHistory extends BaseListChatMessageHis\n \n     await this.collection.deleteOne({ [ID_KEY]: this.sessionId });\n   }\n+\n+  async getAllSessions(): Promise<ChatSession[]> {\n+    await this.initialize();\n+    const documents = await this.collection.find().toArray();\n+\n+    const chatSessions: ChatSession[] = documents.map((doc) => ({\n+      id: doc[ID_KEY],\n+      context: doc.context || {},\n+    }));\n+\n+    return chatSessions;\n+  }\n+\n+  async clearAllSessions() {\n+    await this.initialize();\n+    try {\n+      await this.collection.deleteMany({});\n+    } catch (error) {\n+      console.log(\"Error clearing sessions:\", error);",
        "comment_created_at": "2025-01-12T15:12:23+00:00",
        "comment_author": "crisjy",
        "comment_body": "throw errors for this",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1661598255",
    "pr_number": 5835,
    "pr_file": "libs/langchain-google-common/src/auth.ts",
    "created_at": "2024-07-01T22:27:33+00:00",
    "commented_code": "`Google request failed with status code ${res.status}: ${resText}`\n      );\n      // eslint-disable-next-line @typescript-eslint/no-explicit-any\n      (error as any).response = res;\n      (error as any).details = {",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1661598255",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5835,
        "pr_file": "libs/langchain-google-common/src/auth.ts",
        "discussion_id": "1661598255",
        "commented_code": "@@ -58,15 +73,18 @@ export abstract class GoogleAbstractedFetchClient\n         `Google request failed with status code ${res.status}: ${resText}`\n       );\n       // eslint-disable-next-line @typescript-eslint/no-explicit-any\n-      (error as any).response = res;\n+      (error as any).details = {",
        "comment_created_at": "2024-07-01T22:27:33+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Good to leave `response` directly on the error object - `AsyncCaller` uses fields on it to decide retries.",
        "pr_file_module": null
      }
    ]
  }
]
