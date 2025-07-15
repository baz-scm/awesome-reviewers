---
title: Document API schemas
description: 'Add comprehensive JSDoc comments to all API interfaces, types, and schema
  definitions. This documentation should:


  1. Include links to official external documentation when available'
repository: vercel/ai
label: Documentation
language: TypeScript
comments_count: 5
repository_stars: 15590
---

Add comprehensive JSDoc comments to all API interfaces, types, and schema definitions. This documentation should:

1. Include links to official external documentation when available
2. Describe each property in schema objects to provide context for their use
3. Be placed at the appropriate abstraction level to support inheritance in class hierarchies
4. Include example values where helpful

This practice improves developer experience through enhanced IDE tooltips and makes the code more maintainable by new team members.

Example:

```typescript
/**
 * Web search tool result error content
 * @see https://docs.anthropic.com/en/docs/build-with-claude/tool-use/web-search-tool#errors
 */
export interface AnthropicWebSearchToolResultErrorContent {
  /** Identifies this as a web search tool error response */
  type: 'web_search_tool_result_error';
  
  /** Error code from the API (e.g., 'max_uses_exceeded', 'too_many_requests') */
  error_code: string;
}

// For schemas with multiple properties:
const providerOptionsSchema = z.object({
  /** Language code (ISO-639-1) for transcription, e.g. 'en-US' */
  language: z.string().nullish(),
  
  /** Start position in seconds for partial audio processing */
  audioStartAt: z.number().int().nullish(),
});
```