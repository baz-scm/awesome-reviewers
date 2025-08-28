---
title: Balance organization with constraints
description: When making code organization decisions, consider the broader impact
  beyond just eliminating duplication or following patterns. Sometimes a slightly
  less "clean" solution is preferable when it preserves type safety, maintains clear
  class responsibilities, or avoids exposing unnecessary implementation details.
repository: cloudflare/agents
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 2312
---

When making code organization decisions, consider the broader impact beyond just eliminating duplication or following patterns. Sometimes a slightly less "clean" solution is preferable when it preserves type safety, maintains clear class responsibilities, or avoids exposing unnecessary implementation details.

Key considerations:
- **Type safety over DRY**: Minor code duplication may be acceptable if extraction would require type assertions or null checks
- **Class focus**: Avoid adding functionality to existing classes just for convenience; consider separate specialized classes instead
- **Interface clarity**: Don't implement interfaces that expose methods irrelevant to the class's primary purpose

Example: Instead of extracting common code that would lose TypeScript type information:
```typescript
// Prefer this (preserves type safety)
if (this.#protocol === "sse") {
  this.#transport = new McpSSETransport(() => this.getWebSocket());
  await this.server.connect(this.#transport);
} else if (this.#protocol === "streamable-http") {
  this.#transport = new McpStreamableHttpTransport(/*...*/);
  await this.server.connect(this.#transport);
}

// Over this (loses type information, requires assertions)
this.#transport = this.#protocol === "sse" 
  ? new McpSSETransport(/*...*/) 
  : new McpStreamableHttpTransport(/*...*/);
await this.server.connect(this.#transport!); // Type assertion needed
```

The goal is maintainable code that serves developers well, not just adherence to abstract principles.