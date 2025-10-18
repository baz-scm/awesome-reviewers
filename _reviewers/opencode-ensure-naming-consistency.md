---
title: Ensure naming consistency
description: Maintain consistent naming for the same entities across different contexts
  including code, documentation, APIs, and external systems. When names must differ
  between contexts, implement fallback mechanisms to handle variations gracefully.
repository: sst/opencode
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 28213
---

Maintain consistent naming for the same entities across different contexts including code, documentation, APIs, and external systems. When names must differ between contexts, implement fallback mechanisms to handle variations gracefully.

Key principles:
- Identifiers should match between code exports and documentation (e.g., server names should be "typescript" in both code and docs, not "Typescript" vs "typescript")
- When interfacing with external systems that expect different naming formats, handle variations programmatically rather than forcing users to remember different formats
- For generated identifiers, use consistent patterns that prevent collisions and remain human-readable

Example from codebase:
```typescript
// Handle repository name variations gracefully
const tries = [
  app.repo, // First try with the original repo name
  app.repo.replace(/\.git$/, ""), // If that fails, try without .git suffix
];

// Use consistent server identifiers that match documentation
const servers: Record<string, LSPServer.Info> = LSPServer.getServerIds(); // Use "typescript", not "Typescript"
```

This prevents user confusion and reduces integration issues when the same logical entity has different naming requirements across different systems.