---
title: Match configuration documentation
description: 'Configuration documentation must accurately reflect implementation details
  and behavior. Ensure that:


  1. Code examples in documentation use the exact same property names and structure
  as the actual implementation'
repository: langchain-ai/langchainjs
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 15004
---

Configuration documentation must accurately reflect implementation details and behavior. Ensure that:

1. Code examples in documentation use the exact same property names and structure as the actual implementation
2. Configuration option descriptions explain all behavioral implications, including exceptions and special cases

**Example - Incorrect:**
```typescript
const client = new MultiServerMCPClient({
  mcpServers: {
    'data-processor': {
      command: 'python',
      args: ['data_server.py']
    }
  }
});
```

**Example - Correct:**
```typescript
const client = new MultiServerMCPClient({
  'data-processor': {
    command: 'python',
    args: ['data_server.py']
  }
});
```

When documenting configuration flags like `useStandardContentBlocks`, also include special case behavior (e.g., "audio content always uses standard content blocks regardless of this setting").


[
  {
    "discussion_id": "2103914077",
    "pr_number": 8241,
    "pr_file": "libs/langchain-mcp-adapters/README.md",
    "created_at": "2025-05-23T06:42:58+00:00",
    "commented_code": "| `prefixToolNameWithServerName` | boolean | `true`  | If true, prefixes all tool names with the server name (e.g., `serverName__toolName`) |\n| `additionalToolNamePrefix`     | string  | `mcp`   | Additional prefix to add to tool names (e.g., `prefix__serverName__toolName`)        |\n\n## Tool Timeout Configuration\n\nMCP tools support timeout configuration through LangChain's standard `RunnableConfig` interface. This allows you to set custom timeouts on a per-tool-call basis:\n\n```typescript\nconst client = new MultiServerMCPClient({\n  mcpServers: {\n    'data-processor': {\n      command: 'python',\n      args: ['data_server.py']\n    }",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2103914077",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8241,
        "pr_file": "libs/langchain-mcp-adapters/README.md",
        "discussion_id": "2103914077",
        "commented_code": "@@ -224,6 +224,57 @@ When loading MCP tools either directly through `loadMcpTools` or via `MultiServe\n | `prefixToolNameWithServerName` | boolean | `true`  | If true, prefixes all tool names with the server name (e.g., `serverName__toolName`) |\n | `additionalToolNamePrefix`     | string  | `mcp`   | Additional prefix to add to tool names (e.g., `prefix__serverName__toolName`)        |\n \n+## Tool Timeout Configuration\n+\n+MCP tools support timeout configuration through LangChain's standard `RunnableConfig` interface. This allows you to set custom timeouts on a per-tool-call basis:\n+\n+```typescript\n+const client = new MultiServerMCPClient({\n+  mcpServers: {\n+    'data-processor': {\n+      command: 'python',\n+      args: ['data_server.py']\n+    }",
        "comment_created_at": "2025-05-23T06:42:58+00:00",
        "comment_author": "Copilot",
        "comment_body": "The example uses a `mcpServers` property which doesn\u2019t match the constructor signature shown elsewhere (tests/config expect direct server mappings). It should accept servers directly instead of nesting under `mcpServers`.\n```suggestion\n  'data-processor': {\n    command: 'python',\n    args: ['data_server.py']\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2106472876",
    "pr_number": 8252,
    "pr_file": "libs/langchain-mcp-adapters/README.md",
    "created_at": "2025-05-26T04:07:09+00:00",
    "commented_code": "| `throwOnLoadError`             | boolean | `true`  | Whether to throw an error if a tool fails to load                                    |\n| `prefixToolNameWithServerName` | boolean | `true`  | If true, prefixes all tool names with the server name (e.g., `serverName__toolName`) |\n| `additionalToolNamePrefix`     | string  | `mcp`   | Additional prefix to add to tool names (e.g., `prefix__serverName__toolName`)        |\n| `useStandardContentBlocks`     | boolean | `false` | If true, uses LangChain's standard multimodal content blocks. Defaults to false for backward compatibility; recommended to set true for new applications |",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2106472876",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8252,
        "pr_file": "libs/langchain-mcp-adapters/README.md",
        "discussion_id": "2106472876",
        "commented_code": "@@ -223,6 +223,7 @@ When loading MCP tools either directly through `loadMcpTools` or via `MultiServe\n | `throwOnLoadError`             | boolean | `true`  | Whether to throw an error if a tool fails to load                                    |\n | `prefixToolNameWithServerName` | boolean | `true`  | If true, prefixes all tool names with the server name (e.g., `serverName__toolName`) |\n | `additionalToolNamePrefix`     | string  | `mcp`   | Additional prefix to add to tool names (e.g., `prefix__serverName__toolName`)        |\n+| `useStandardContentBlocks`     | boolean | `false` | If true, uses LangChain's standard multimodal content blocks. Defaults to false for backward compatibility; recommended to set true for new applications |",
        "comment_created_at": "2025-05-26T04:07:09+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider emphasizing that audio content is always processed using standard content blocks regardless of the flag, to clarify the behavioral difference between audio and other content types.",
        "pr_file_module": null
      },
      {
        "comment_id": "2106473673",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8252,
        "pr_file": "libs/langchain-mcp-adapters/README.md",
        "discussion_id": "2106472876",
        "commented_code": "@@ -223,6 +223,7 @@ When loading MCP tools either directly through `loadMcpTools` or via `MultiServe\n | `throwOnLoadError`             | boolean | `true`  | Whether to throw an error if a tool fails to load                                    |\n | `prefixToolNameWithServerName` | boolean | `true`  | If true, prefixes all tool names with the server name (e.g., `serverName__toolName`) |\n | `additionalToolNamePrefix`     | string  | `mcp`   | Additional prefix to add to tool names (e.g., `prefix__serverName__toolName`)        |\n+| `useStandardContentBlocks`     | boolean | `false` | If true, uses LangChain's standard multimodal content blocks. Defaults to false for backward compatibility; recommended to set true for new applications |",
        "comment_created_at": "2025-05-26T04:08:19+00:00",
        "comment_author": "benjamincburns",
        "comment_body": "Covered elsewhere.",
        "pr_file_module": null
      }
    ]
  }
]
