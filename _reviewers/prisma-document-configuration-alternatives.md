---
title: Document configuration alternatives
description: When documenting configuration setup, provide multiple formats and approaches
  to accommodate different tools, platforms, and environments. Include both the base
  command and tool-specific configuration examples when applicable.
repository: prisma/prisma
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 42967
---

When documenting configuration setup, provide multiple formats and approaches to accommodate different tools, platforms, and environments. Include both the base command and tool-specific configuration examples when applicable.

This ensures users can successfully configure the system regardless of their specific environment or tooling choices. For example, when documenting MCP server setup, provide both the CLI command and JSON configuration:

```bash
npx prisma mcp
```

And the JSON configuration for AI tools:

```json
{
  "mcpServers": {
    "Prisma": {
      "command": "npx",
      "args": ["-y", "prisma", "mcp"]
    }
  }
}
```

Additionally, clearly document environment-specific behaviors and requirements, such as Windows-specific installation steps or path resolution differences, to help users understand and troubleshoot platform-specific issues.