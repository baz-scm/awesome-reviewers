---
title: Eliminate redundant code
description: Simplify code by eliminating redundancy and unnecessary complexity. This
  improves readability, reduces potential bugs, and makes the codebase easier to maintain.
repository: langchain-ai/langchainjs
label: Code Style
language: Typescript
comments_count: 4
repository_stars: 15004
---

Simplify code by eliminating redundancy and unnecessary complexity. This improves readability, reduces potential bugs, and makes the codebase easier to maintain.

Some key practices to follow:

1. **Avoid unnecessary object creation**: Don't create objects that might be discarded immediately.
```typescript
// Instead of this:
let requestOptions: RequestOptions | undefined = {
  ...(config?.timeout ? { timeout: config.timeout } : {}),
  ...(config?.signal ? { signal: config.signal } : {}),
};

if (Object.keys(requestOptions).length === 0) {
  requestOptions = undefined;
}

// Do this:
const requestOptions: RequestOptions | undefined = config?.timeout || config?.signal
  ? { timeout: config.timeout, signal: config.signal }
  : undefined;
```

2. **Remove redundant await in returns**: In async functions, avoid using `await` when returning a promise.
```typescript
// Instead of this:
async function getData() {
  return await fetchData();
}

// Do this:
async function getData() {
  return fetchData();
}
```

3. **Use concise array methods**: Many array methods have default parameters you can omit.
```typescript
// Instead of this:
return embeddings.flat(1);

// Do this:
return embeddings.flat();
```

4. **Don't declare class properties only used in constructors**: If a property is only accessed inside the class constructor, it doesn't need to be a class property.
```typescript
// Instead of this:
class MyClass {
  json = false;
  
  constructor() {
    if (this.json) {
      // do something
    }
  }
}

// Do this:
class MyClass {
  constructor() {
    const json = false;
    if (json) {
      // do something
    }
  }
}
```

Eliminating redundancy leads to cleaner, more maintainable code that's easier to review and less prone to errors.


[
  {
    "discussion_id": "2106380214",
    "pr_number": 8241,
    "pr_file": "libs/langchain-mcp-adapters/src/tools.ts",
    "created_at": "2025-05-26T01:25:52+00:00",
    "commented_code": "* @param client - The MCP client\n * @param toolName - The name of the tool (forwarded to the client)\n * @param args - The arguments to pass to the tool\n * @param config - Optional RunnableConfig with timeout settings\n * @returns A tuple of [textContent, nonTextContent]\n */\nasync function _callTool(\n  serverName: string,\n  toolName: string,\n  client: Client,\n  args: Record<string, unknown>\n  args: Record<string, unknown>,\n  config?: RunnableConfig\n): Promise<[MessageContent, EmbeddedResource[]]> {\n  let result: CallToolResult;\n  try {\n    getDebugLog()(`INFO: Calling tool ${toolName}(${JSON.stringify(args)})`);\n    result = (await client.callTool({\n      name: toolName,\n      arguments: args,\n    })) as CallToolResult;\n\n    // Extract timeout from RunnableConfig and pass to MCP SDK\n    let requestOptions: RequestOptions | undefined = {\n      ...(config?.timeout ? { timeout: config.timeout } : {}),\n      ...(config?.signal ? { signal: config.signal } : {}),\n    };\n\n    if (Object.keys(requestOptions).length === 0) {\n      requestOptions = undefined;\n    }",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2106380214",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8241,
        "pr_file": "libs/langchain-mcp-adapters/src/tools.ts",
        "discussion_id": "2106380214",
        "commented_code": "@@ -161,21 +163,38 @@ async function _convertCallToolResult(\n  * @param client - The MCP client\n  * @param toolName - The name of the tool (forwarded to the client)\n  * @param args - The arguments to pass to the tool\n+ * @param config - Optional RunnableConfig with timeout settings\n  * @returns A tuple of [textContent, nonTextContent]\n  */\n async function _callTool(\n   serverName: string,\n   toolName: string,\n   client: Client,\n-  args: Record<string, unknown>\n+  args: Record<string, unknown>,\n+  config?: RunnableConfig\n ): Promise<[MessageContent, EmbeddedResource[]]> {\n   let result: CallToolResult;\n   try {\n     getDebugLog()(`INFO: Calling tool ${toolName}(${JSON.stringify(args)})`);\n-    result = (await client.callTool({\n-      name: toolName,\n-      arguments: args,\n-    })) as CallToolResult;\n+\n+    // Extract timeout from RunnableConfig and pass to MCP SDK\n+    let requestOptions: RequestOptions | undefined = {\n+      ...(config?.timeout ? { timeout: config.timeout } : {}),\n+      ...(config?.signal ? { signal: config.signal } : {}),\n+    };\n+\n+    if (Object.keys(requestOptions).length === 0) {\n+      requestOptions = undefined;\n+    }\n+",
        "comment_created_at": "2025-05-26T01:25:52+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] The logic to build and then drop an empty `requestOptions` object adds cognitive overhead. You could simplify by only constructing `requestOptions` when `config?.timeout` or `config?.signal` is present, e.g.: `const requestOptions = config ? { timeout: config.timeout, signal: config.signal } : undefined;`.\n```suggestion\n    const requestOptions: RequestOptions | undefined = config?.timeout || config?.signal\n      ? { timeout: config.timeout, signal: config.signal }\n      : undefined;\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2106472869",
    "pr_number": 8252,
    "pr_file": "libs/langchain-mcp-adapters/src/tools.ts",
    "created_at": "2025-05-26T04:07:08+00:00",
    "commented_code": "}\n\n    const result = await client.callTool(...callToolArgs);\n    return _convertCallToolResult(serverName, toolName, result, client);\n    return await _convertCallToolResult({",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2106472869",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8252,
        "pr_file": "libs/langchain-mcp-adapters/src/tools.ts",
        "discussion_id": "2106472869",
        "commented_code": "@@ -207,7 +289,13 @@ async function _callTool(\n     }\n \n     const result = await client.callTool(...callToolArgs);\n-    return _convertCallToolResult(serverName, toolName, result, client);\n+    return await _convertCallToolResult({",
        "comment_created_at": "2025-05-26T04:07:08+00:00",
        "comment_author": "Copilot",
        "comment_body": "In an async function, 'return await' is generally redundant. Consider returning the promise directly to simplify the code.\n```suggestion\n    return _convertCallToolResult({\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1583887935",
    "pr_number": 5251,
    "pr_file": "libs/langchain-azure-openai/src/embeddings.ts",
    "created_at": "2024-04-29T23:11:30+00:00",
    "commented_code": "const batchRequests = batches.map((batch) => this.getEmbeddings(batch));\n    const embeddings = await Promise.all(batchRequests);\n\n    return embeddings;\n    return embeddings.flat(1);",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1583887935",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5251,
        "pr_file": "libs/langchain-azure-openai/src/embeddings.ts",
        "discussion_id": "1583887935",
        "commented_code": "@@ -135,18 +135,18 @@ export class AzureOpenAIEmbeddings\n \n     const batchRequests = batches.map((batch) => this.getEmbeddings(batch));\n     const embeddings = await Promise.all(batchRequests);\n-\n-    return embeddings;\n+    return embeddings.flat(1);",
        "comment_created_at": "2024-04-29T23:11:30+00:00",
        "comment_author": "bracesproul",
        "comment_body": "Nit, defaults to 1 so this can be dropped.\r\n```suggestion\r\n    return embeddings.flat();\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1719005999",
    "pr_number": 6519,
    "pr_file": "libs/langchain-google-genai/src/chat_models.ts",
    "created_at": "2024-08-15T21:16:00+00:00",
    "commented_code": "streamUsage = true;\n\n  json = false",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1719005999",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 6519,
        "pr_file": "libs/langchain-google-genai/src/chat_models.ts",
        "discussion_id": "1719005999",
        "commented_code": "@@ -244,6 +247,8 @@ export class ChatGoogleGenerativeAI\n \n   streamUsage = true;\n \n+  json = false",
        "comment_created_at": "2024-08-15T21:16:00+00:00",
        "comment_author": "bracesproul",
        "comment_body": "If this is only accessed inside the class constructor we don't need to make it a class property.\r\n```suggestion\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
