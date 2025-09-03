---
title: AI documentation clarity
description: Ensure AI-related documentation, comments, and explanations are clear,
  accurate, and well-structured. This includes fixing spelling errors, using precise
  terminology, adding necessary context about experimental features, and employing
  active voice for better readability.
repository: angular/angular
label: AI
language: Markdown
comments_count: 5
repository_stars: 98611
---

Ensure AI-related documentation, comments, and explanations are clear, accurate, and well-structured. This includes fixing spelling errors, using precise terminology, adding necessary context about experimental features, and employing active voice for better readability.

Key practices:
- Fix spelling errors immediately (e.g., "asynchronous" not "asyncronous") as they can block merges
- Use precise, professional language ("preferred" instead of "favorite")
- Add context and links for technical concepts (e.g., link to MCP documentation when mentioning Model Context Protocol)
- Use active voice for clearer explanations ("You can configure LLM APIs" instead of "LLM APIs can be configured")
- Simplify complex technical explanations while maintaining accuracy
- Mark experimental features clearly to set proper expectations

Example improvement:
```
// Before: "LLM APIs can be configured to return structured data"
// After: "You can configure LLM APIs to return structured data"

// Before: "The Angular CLI includes a Model Context Protocol (MCP) server"
// After: "The Angular CLI includes an experimental [Model Context Protocol (MCP) server](https://modelcontextprotocol.io/)"
```

Clear documentation is especially critical for AI features as they often involve complex concepts, experimental APIs, and emerging patterns that developers may be unfamiliar with.