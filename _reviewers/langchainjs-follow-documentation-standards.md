---
title: Follow documentation standards
description: Ensure all documentation follows established templates and includes required
  sections. When referencing components, add links to their documentation pages. Documentation
  for each component type (like LLMs or vector stores) should follow its specific
  template format and include standard sections such as "Overview" with links to conceptual
  guides and...
repository: langchain-ai/langchainjs
label: Documentation
language: Other
comments_count: 5
repository_stars: 15004
---

Ensure all documentation follows established templates and includes required sections. When referencing components, add links to their documentation pages. Documentation for each component type (like LLMs or vector stores) should follow its specific template format and include standard sections such as "Overview" with links to conceptual guides and reference tables.

When a component is mentioned in documentation text, include a hyperlink to its own documentation:

```typescript
// Good example with proper cross-referencing
/**
 * The Semantic Cache feature leverages [AzureCosmosDBNoSQLVectorStore](/docs/integrations/vectorstores/azure_cosmosdb_nosql) 
 * which stores vector embeddings of cached prompts for similarity-based searches.
 * 
 * @see For more details, refer to the [Vector Store conceptual guide](/docs/concepts/vector_stores)
 */
```

Complete documentation should exist for all public APIs and referenced components. If documentation for a referenced component is missing (like `JsonOutputFunctionsParser`), create it before finalizing the referencing documentation.
