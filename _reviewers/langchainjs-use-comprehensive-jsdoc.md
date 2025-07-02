---
title: Use comprehensive JSDoc
description: 'Always use JSDoc format (`/** */`) instead of regular comments (`//`)
  for documenting classes, functions, and interfaces. Documentation should be comprehensive,
  including:'
repository: langchain-ai/langchainjs
label: Documentation
language: Typescript
comments_count: 7
repository_stars: 15004
---

Always use JSDoc format (`/** */`) instead of regular comments (`//`) for documenting classes, functions, and interfaces. Documentation should be comprehensive, including:

1. Clear purpose descriptions
2. Usage examples where appropriate
3. Proper tags like `@internal` for non-public API elements
4. Cross-references using `{@link ...}` syntax
5. Migration paths for deprecated features

This ensures that documentation integrates correctly with API reference generators and provides developers with sufficient context.

**Example - Before:**
```typescript
// this class uses your clientId, clientSecret and redirectUri
// to get access token and refresh token, if you already have them,
// you can use AuthFlowToken or AuthFlowRefresh instead
export class AuthFlow {
  // ...
}
```

**Example - After:**
```typescript
/**
 * Authentication flow for obtaining access and refresh tokens using clientId,
 * clientSecret and redirectUri.
 * 
 * @example
 * const auth = new AuthFlow({
 *   clientId: process.env.CLIENT_ID,
 *   clientSecret: process.env.CLIENT_SECRET,
 *   redirectUri: "http://localhost:3000/callback"
 * });
 * const tokens = await auth.getTokens();
 * 
 * @see If you already have tokens, consider using {@link AuthFlowToken} or
 * {@link AuthFlowRefresh} instead.
 */
export class AuthFlow {
  // ...
}
```


[
  {
    "discussion_id": "1417964024",
    "pr_number": 3465,
    "pr_file": "langchain/src/tools/outlook/authFlowREST.ts",
    "created_at": "2023-12-06T20:52:16+00:00",
    "commented_code": "import * as http from \"http\";\nimport * as url from \"url\";\nimport { AuthFlowBase } from \"./authFlowBase.js\";\nimport { getEnvironmentVariable } from \"../../util/env.js\";\n\ninterface AccessTokenResponse {\n  access_token: string;\n  refresh_token: string;\n}\n\n// this class uses your clientId, clientSecret and redirectUri\n// to get access token and refresh token, if you already have them,\n// you can use AuthFlowToken or AuthFlowRefresh instead",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1417964024",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3465,
        "pr_file": "langchain/src/tools/outlook/authFlowREST.ts",
        "discussion_id": "1417964024",
        "commented_code": "@@ -0,0 +1,205 @@\n+import * as http from \"http\";\n+import * as url from \"url\";\n+import { AuthFlowBase } from \"./authFlowBase.js\";\n+import { getEnvironmentVariable } from \"../../util/env.js\";\n+\n+interface AccessTokenResponse {\n+  access_token: string;\n+  refresh_token: string;\n+}\n+\n+// this class uses your clientId, clientSecret and redirectUri\n+// to get access token and refresh token, if you already have them,\n+// you can use AuthFlowToken or AuthFlowRefresh instead",
        "comment_created_at": "2023-12-06T20:52:16+00:00",
        "comment_author": "bracesproul",
        "comment_body": "This should be a JSDoc so devs & our api refs can get the description properly",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1418002088",
    "pr_number": 3465,
    "pr_file": "langchain/src/tools/outlook/authFlowToken.ts",
    "created_at": "2023-12-06T21:33:05+00:00",
    "commented_code": "import { AuthFlowBase } from \"./authFlowBase.js\";\nimport { getEnvironmentVariable } from \"../../util/env.js\";\n\ninterface AccessTokenResponse {\n  access_token: string;\n  refresh_token: string;\n}\n\n// if you have the token, and no need to refresh it, warning: token expires in 1 hour",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1418002088",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 3465,
        "pr_file": "langchain/src/tools/outlook/authFlowToken.ts",
        "discussion_id": "1418002088",
        "commented_code": "@@ -0,0 +1,103 @@\n+import { AuthFlowBase } from \"./authFlowBase.js\";\n+import { getEnvironmentVariable } from \"../../util/env.js\";\n+\n+interface AccessTokenResponse {\n+  access_token: string;\n+  refresh_token: string;\n+}\n+\n+// if you have the token, and no need to refresh it, warning: token expires in 1 hour",
        "comment_created_at": "2023-12-06T21:33:05+00:00",
        "comment_author": "bracesproul",
        "comment_body": "Convert to JSDoc and give more of an overview as to what this class can be used for",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2152847821",
    "pr_number": 8379,
    "pr_file": "langchain-core/src/utils/js-sha1/hash.ts",
    "created_at": "2025-06-17T17:54:53+00:00",
    "commented_code": "return buffer;\n};\n\n/**\n * @deprecated Use `makeDefaultKeyEncoder()` to create a custom key encoder.\n * This function will be removed in a future version.\n */\nexport const insecureHash = (message) => {\n  console.warn(",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2152847821",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8379,
        "pr_file": "langchain-core/src/utils/js-sha1/hash.ts",
        "discussion_id": "2152847821",
        "commented_code": "@@ -412,6 +412,19 @@ Sha1.prototype.arrayBuffer = function () {\n   return buffer;\n };\n \n+/**\n+ * @deprecated Use `makeDefaultKeyEncoder()` to create a custom key encoder.\n+ * This function will be removed in a future version.\n+ */\n export const insecureHash = (message) => {\n+  console.warn(",
        "comment_created_at": "2025-06-17T17:54:53+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Let's just log this once on initial call to avoid flooding the console and add some example code",
        "pr_file_module": null
      },
      {
        "comment_id": "2152875547",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8379,
        "pr_file": "langchain-core/src/utils/js-sha1/hash.ts",
        "discussion_id": "2152847821",
        "commented_code": "@@ -412,6 +412,19 @@ Sha1.prototype.arrayBuffer = function () {\n   return buffer;\n };\n \n+/**\n+ * @deprecated Use `makeDefaultKeyEncoder()` to create a custom key encoder.\n+ * This function will be removed in a future version.\n+ */\n export const insecureHash = (message) => {\n+  console.warn(",
        "comment_created_at": "2025-06-17T18:10:07+00:00",
        "comment_author": "manekinekko",
        "comment_body": "Fixed.",
        "pr_file_module": null
      },
      {
        "comment_id": "2152877086",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8379,
        "pr_file": "langchain-core/src/utils/js-sha1/hash.ts",
        "discussion_id": "2152847821",
        "commented_code": "@@ -412,6 +412,19 @@ Sha1.prototype.arrayBuffer = function () {\n   return buffer;\n };\n \n+/**\n+ * @deprecated Use `makeDefaultKeyEncoder()` to create a custom key encoder.\n+ * This function will be removed in a future version.\n+ */\n export const insecureHash = (message) => {\n+  console.warn(",
        "comment_created_at": "2025-06-17T18:11:06+00:00",
        "comment_author": "manekinekko",
        "comment_body": "> add some example code\r\n\r\nCan you elaborate on which example code you'd like to be added?",
        "pr_file_module": null
      },
      {
        "comment_id": "2152879610",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8379,
        "pr_file": "langchain-core/src/utils/js-sha1/hash.ts",
        "discussion_id": "2152847821",
        "commented_code": "@@ -412,6 +412,19 @@ Sha1.prototype.arrayBuffer = function () {\n   return buffer;\n };\n \n+/**\n+ * @deprecated Use `makeDefaultKeyEncoder()` to create a custom key encoder.\n+ * This function will be removed in a future version.\n+ */\n export const insecureHash = (message) => {\n+  console.warn(",
        "comment_created_at": "2025-06-17T18:12:34+00:00",
        "comment_author": "manekinekko",
        "comment_body": "@jacoblee93 can we maybe link to some docs?",
        "pr_file_module": null
      },
      {
        "comment_id": "2155188698",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8379,
        "pr_file": "langchain-core/src/utils/js-sha1/hash.ts",
        "discussion_id": "2152847821",
        "commented_code": "@@ -412,6 +412,19 @@ Sha1.prototype.arrayBuffer = function () {\n   return buffer;\n };\n \n+/**\n+ * @deprecated Use `makeDefaultKeyEncoder()` to create a custom key encoder.\n+ * This function will be removed in a future version.\n+ */\n export const insecureHash = (message) => {\n+  console.warn(",
        "comment_created_at": "2025-06-18T17:54:07+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Ah right... this is used in multiple places\r\n\r\n@hntrl maybe let's make a small docs page with agnostic info here?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2065677698",
    "pr_number": 8090,
    "pr_file": "libs/langchain-openai/src/chat_models.ts",
    "created_at": "2025-04-29T07:17:40+00:00",
    "commented_code": "/**\n   * Constrains effort on reasoning for reasoning models. Currently supported values are low, medium, and high.\n   * Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.\n   *\n   * @deprecated Use `reasoning` object instead.",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2065677698",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8090,
        "pr_file": "libs/langchain-openai/src/chat_models.ts",
        "discussion_id": "2065677698",
        "commented_code": "@@ -1024,9 +1050,19 @@ export interface ChatOpenAICallOptions\n   /**\n    * Constrains effort on reasoning for reasoning models. Currently supported values are low, medium, and high.\n    * Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.\n+   *\n+   * @deprecated Use `reasoning` object instead.",
        "comment_created_at": "2025-04-29T07:17:40+00:00",
        "comment_author": "benjamincburns",
        "comment_body": "use `{@link ... }` syntax",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2050989297",
    "pr_number": 8042,
    "pr_file": "langchain-core/src/language_models/chat_models.ts",
    "created_at": "2025-04-18T18:45:37+00:00",
    "commented_code": "});\n}\n\n/**\n * \ndef _format_for_tracing(messages: list[BaseMessage]) -> list[BaseMessage]:\n    \"\"\"Format messages for tracing in on_chat_model_start.\n    For backward compatibility, we update image content blocks to OpenAI Chat\n    Completions format.\n    Args:\n        messages: List of messages to format.\n    Returns:\n        List of messages formatted for tracing.\n    \"\"\"\n    messages_to_trace = []\n    for message in messages:\n        message_to_trace = message\n        if isinstance(message.content, list):\n            for idx, block in enumerate(message.content):\n                if (\n                    isinstance(block, dict)\n                    and block.get(\"type\") == \"image\"\n                    and is_data_content_block(block)\n                ):\n                    if message_to_trace is message:\n                        message_to_trace = message.model_copy()\n                        # Also shallow-copy content\n                        message_to_trace.content = list(message_to_trace.content)\n\n                    message_to_trace.content[idx] = (  # type: ignore[index]  # mypy confused by .model_copy\n                        convert_to_openai_image_block(block)\n                    )\n        messages_to_trace.append(message_to_trace)\n\n    return messages_to_trace\n */\n\nfunction _formatForTracing(messages: BaseMessage[]): BaseMessage[] {",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2050989297",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8042,
        "pr_file": "langchain-core/src/language_models/chat_models.ts",
        "discussion_id": "2050989297",
        "commented_code": "@@ -130,6 +132,73 @@ export function createChatMessageChunkEncoderStream() {\n   });\n }\n \n+/**\n+ * \n+def _format_for_tracing(messages: list[BaseMessage]) -> list[BaseMessage]:\n+    \"\"\"Format messages for tracing in on_chat_model_start.\n+    For backward compatibility, we update image content blocks to OpenAI Chat\n+    Completions format.\n+    Args:\n+        messages: List of messages to format.\n+    Returns:\n+        List of messages formatted for tracing.\n+    \"\"\"\n+    messages_to_trace = []\n+    for message in messages:\n+        message_to_trace = message\n+        if isinstance(message.content, list):\n+            for idx, block in enumerate(message.content):\n+                if (\n+                    isinstance(block, dict)\n+                    and block.get(\"type\") == \"image\"\n+                    and is_data_content_block(block)\n+                ):\n+                    if message_to_trace is message:\n+                        message_to_trace = message.model_copy()\n+                        # Also shallow-copy content\n+                        message_to_trace.content = list(message_to_trace.content)\n+\n+                    message_to_trace.content[idx] = (  # type: ignore[index]  # mypy confused by .model_copy\n+                        convert_to_openai_image_block(block)\n+                    )\n+        messages_to_trace.append(message_to_trace)\n+\n+    return messages_to_trace\n+ */\n+\n+function _formatForTracing(messages: BaseMessage[]): BaseMessage[] {",
        "comment_created_at": "2025-04-18T18:45:37+00:00",
        "comment_author": "bracesproul",
        "comment_body": "jsdoc would be nice explaining what it's doing",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2054972084",
    "pr_number": 8053,
    "pr_file": "langchain/src/chat_models/universal.ts",
    "created_at": "2025-04-22T22:21:27+00:00",
    "commented_code": "queuedMethodOperations?: Record<string, any>;\n}\n\nclass _ConfigurableModel<\n/**\n * Internal class used to create chat models.",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2054972084",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8053,
        "pr_file": "langchain/src/chat_models/universal.ts",
        "discussion_id": "2054972084",
        "commented_code": "@@ -238,7 +238,10 @@ interface ConfigurableModelFields extends BaseChatModelParams {\n   queuedMethodOperations?: Record<string, any>;\n }\n \n-class _ConfigurableModel<\n+/**\n+ * Internal class used to create chat models.",
        "comment_created_at": "2025-04-22T22:21:27+00:00",
        "comment_author": "benjamincburns",
        "comment_body": "Not sure if this is set up for langchain yet, but it's good practice to use the `@internal` tsdoc tag on internal structures, that way we don't need to treat them as public for the purpose of breaking changes.",
        "pr_file_module": null
      },
      {
        "comment_id": "2054972335",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8053,
        "pr_file": "langchain/src/chat_models/universal.ts",
        "discussion_id": "2054972084",
        "commented_code": "@@ -238,7 +238,10 @@ interface ConfigurableModelFields extends BaseChatModelParams {\n   queuedMethodOperations?: Record<string, any>;\n }\n \n-class _ConfigurableModel<\n+/**\n+ * Internal class used to create chat models.",
        "comment_created_at": "2025-04-22T22:21:43+00:00",
        "comment_author": "benjamincburns",
        "comment_body": "```suggestion\r\n * Internal class used to create chat models.\r\n *\r\n * @internal\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2004654421",
    "pr_number": 7852,
    "pr_file": "libs/langchain-google-cloud-sql-pg/src/engine.ts",
    "created_at": "2025-03-20T01:54:51+00:00",
    "commented_code": "import { AuthTypes, Connector, IpAddressTypes } from \"@google-cloud/cloud-sql-connector\";\nimport { GoogleAuth } from \"google-auth-library\";\nimport knex from \"knex\";\nimport { getIAMPrincipalEmail } from \"./utils/utils.js\";\n\nexport interface PostgresEngineArgs {\n  ipType?: IpAddressTypes,\n  user?: string,\n  password?: string,\n  iamAccountEmail?: string,\n}\n\nexport interface VectorStoreTableArgs {\n  schemaName?: string,\n  contentColumn?: string,\n  embeddingColumn?: string,\n  metadataColumns?: Column[],\n  metadataJsonColumn?: string,\n  idColumn?: string | Column,\n  overwriteExisting?: boolean,\n  storeMetadata?: boolean\n}\n\nexport class Column {\n  name: string;\n\n  dataType: string;\n\n  nullable: boolean;\n\n  constructor(name: string, dataType: string, nullable: boolean = true) {\n    this.name = name;\n    this.dataType = dataType;\n    this.nullable = nullable;\n\n    this.postInitilization()\n  }\n\n  private postInitilization() {\n    if (typeof this.name !== \"string\") {\n      throw Error(\"Column name must be type string\");\n    }\n\n    if (typeof this.dataType !== \"string\") {\n      throw Error(\"Column data_type must be type string\");\n    }\n\n  }\n}\n\nconst USER_AGENT = \"langchain-google-cloud-sql-pg-js\";\n\nexport class PostgresEngine {",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2004654421",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7852,
        "pr_file": "libs/langchain-google-cloud-sql-pg/src/engine.ts",
        "discussion_id": "2004654421",
        "commented_code": "@@ -0,0 +1,271 @@\n+import { AuthTypes, Connector, IpAddressTypes } from \"@google-cloud/cloud-sql-connector\";\n+import { GoogleAuth } from \"google-auth-library\";\n+import knex from \"knex\";\n+import { getIAMPrincipalEmail } from \"./utils/utils.js\";\n+\n+export interface PostgresEngineArgs {\n+  ipType?: IpAddressTypes,\n+  user?: string,\n+  password?: string,\n+  iamAccountEmail?: string,\n+}\n+\n+export interface VectorStoreTableArgs {\n+  schemaName?: string,\n+  contentColumn?: string,\n+  embeddingColumn?: string,\n+  metadataColumns?: Column[],\n+  metadataJsonColumn?: string,\n+  idColumn?: string | Column,\n+  overwriteExisting?: boolean,\n+  storeMetadata?: boolean\n+}\n+\n+export class Column {\n+  name: string;\n+\n+  dataType: string;\n+\n+  nullable: boolean;\n+\n+  constructor(name: string, dataType: string, nullable: boolean = true) {\n+    this.name = name;\n+    this.dataType = dataType;\n+    this.nullable = nullable;\n+\n+    this.postInitilization()\n+  }\n+\n+  private postInitilization() {\n+    if (typeof this.name !== \"string\") {\n+      throw Error(\"Column name must be type string\");\n+    }\n+\n+    if (typeof this.dataType !== \"string\") {\n+      throw Error(\"Column data_type must be type string\");\n+    }\n+\n+  }\n+}\n+\n+const USER_AGENT = \"langchain-google-cloud-sql-pg-js\";\n+\n+export class PostgresEngine {",
        "comment_created_at": "2025-03-20T01:54:51+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "nit: Add docstring with usage example",
        "pr_file_module": null
      },
      {
        "comment_id": "2004658794",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7852,
        "pr_file": "libs/langchain-google-cloud-sql-pg/src/engine.ts",
        "discussion_id": "2004654421",
        "commented_code": "@@ -0,0 +1,271 @@\n+import { AuthTypes, Connector, IpAddressTypes } from \"@google-cloud/cloud-sql-connector\";\n+import { GoogleAuth } from \"google-auth-library\";\n+import knex from \"knex\";\n+import { getIAMPrincipalEmail } from \"./utils/utils.js\";\n+\n+export interface PostgresEngineArgs {\n+  ipType?: IpAddressTypes,\n+  user?: string,\n+  password?: string,\n+  iamAccountEmail?: string,\n+}\n+\n+export interface VectorStoreTableArgs {\n+  schemaName?: string,\n+  contentColumn?: string,\n+  embeddingColumn?: string,\n+  metadataColumns?: Column[],\n+  metadataJsonColumn?: string,\n+  idColumn?: string | Column,\n+  overwriteExisting?: boolean,\n+  storeMetadata?: boolean\n+}\n+\n+export class Column {\n+  name: string;\n+\n+  dataType: string;\n+\n+  nullable: boolean;\n+\n+  constructor(name: string, dataType: string, nullable: boolean = true) {\n+    this.name = name;\n+    this.dataType = dataType;\n+    this.nullable = nullable;\n+\n+    this.postInitilization()\n+  }\n+\n+  private postInitilization() {\n+    if (typeof this.name !== \"string\") {\n+      throw Error(\"Column name must be type string\");\n+    }\n+\n+    if (typeof this.dataType !== \"string\") {\n+      throw Error(\"Column data_type must be type string\");\n+    }\n+\n+  }\n+}\n+\n+const USER_AGENT = \"langchain-google-cloud-sql-pg-js\";\n+\n+export class PostgresEngine {",
        "comment_created_at": "2025-03-20T01:58:56+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Might be nice to have chat history/vectorstore classes just accept params to instantiate an engine on init in addition to taking a full engine class for connection reuse so that the user has one less import/abstraction to worry about",
        "pr_file_module": null
      },
      {
        "comment_id": "2008312551",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7852,
        "pr_file": "libs/langchain-google-cloud-sql-pg/src/engine.ts",
        "discussion_id": "2004654421",
        "commented_code": "@@ -0,0 +1,271 @@\n+import { AuthTypes, Connector, IpAddressTypes } from \"@google-cloud/cloud-sql-connector\";\n+import { GoogleAuth } from \"google-auth-library\";\n+import knex from \"knex\";\n+import { getIAMPrincipalEmail } from \"./utils/utils.js\";\n+\n+export interface PostgresEngineArgs {\n+  ipType?: IpAddressTypes,\n+  user?: string,\n+  password?: string,\n+  iamAccountEmail?: string,\n+}\n+\n+export interface VectorStoreTableArgs {\n+  schemaName?: string,\n+  contentColumn?: string,\n+  embeddingColumn?: string,\n+  metadataColumns?: Column[],\n+  metadataJsonColumn?: string,\n+  idColumn?: string | Column,\n+  overwriteExisting?: boolean,\n+  storeMetadata?: boolean\n+}\n+\n+export class Column {\n+  name: string;\n+\n+  dataType: string;\n+\n+  nullable: boolean;\n+\n+  constructor(name: string, dataType: string, nullable: boolean = true) {\n+    this.name = name;\n+    this.dataType = dataType;\n+    this.nullable = nullable;\n+\n+    this.postInitilization()\n+  }\n+\n+  private postInitilization() {\n+    if (typeof this.name !== \"string\") {\n+      throw Error(\"Column name must be type string\");\n+    }\n+\n+    if (typeof this.dataType !== \"string\") {\n+      throw Error(\"Column data_type must be type string\");\n+    }\n+\n+  }\n+}\n+\n+const USER_AGENT = \"langchain-google-cloud-sql-pg-js\";\n+\n+export class PostgresEngine {",
        "comment_created_at": "2025-03-21T20:48:26+00:00",
        "comment_author": "averikitsch",
        "comment_body": "I will add docstrings. The engine is a shared object so the connection pool is shared. This is a postgres best practice.",
        "pr_file_module": null
      },
      {
        "comment_id": "2009501988",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 7852,
        "pr_file": "libs/langchain-google-cloud-sql-pg/src/engine.ts",
        "discussion_id": "2004654421",
        "commented_code": "@@ -0,0 +1,271 @@\n+import { AuthTypes, Connector, IpAddressTypes } from \"@google-cloud/cloud-sql-connector\";\n+import { GoogleAuth } from \"google-auth-library\";\n+import knex from \"knex\";\n+import { getIAMPrincipalEmail } from \"./utils/utils.js\";\n+\n+export interface PostgresEngineArgs {\n+  ipType?: IpAddressTypes,\n+  user?: string,\n+  password?: string,\n+  iamAccountEmail?: string,\n+}\n+\n+export interface VectorStoreTableArgs {\n+  schemaName?: string,\n+  contentColumn?: string,\n+  embeddingColumn?: string,\n+  metadataColumns?: Column[],\n+  metadataJsonColumn?: string,\n+  idColumn?: string | Column,\n+  overwriteExisting?: boolean,\n+  storeMetadata?: boolean\n+}\n+\n+export class Column {\n+  name: string;\n+\n+  dataType: string;\n+\n+  nullable: boolean;\n+\n+  constructor(name: string, dataType: string, nullable: boolean = true) {\n+    this.name = name;\n+    this.dataType = dataType;\n+    this.nullable = nullable;\n+\n+    this.postInitilization()\n+  }\n+\n+  private postInitilization() {\n+    if (typeof this.name !== \"string\") {\n+      throw Error(\"Column name must be type string\");\n+    }\n+\n+    if (typeof this.dataType !== \"string\") {\n+      throw Error(\"Column data_type must be type string\");\n+    }\n+\n+  }\n+}\n+\n+const USER_AGENT = \"langchain-google-cloud-sql-pg-js\";\n+\n+export class PostgresEngine {",
        "comment_created_at": "2025-03-24T05:52:27+00:00",
        "comment_author": "jacoblee93",
        "comment_body": "Ok, sounds good. Yeah definitely better to do it this way for prod, just more pieces and classes to set up for getting started",
        "pr_file_module": null
      }
    ]
  }
]
