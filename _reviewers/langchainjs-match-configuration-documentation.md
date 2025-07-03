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
