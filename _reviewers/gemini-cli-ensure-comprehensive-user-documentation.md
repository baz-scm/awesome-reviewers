---
title: Ensure comprehensive user documentation
description: All user-facing features, APIs, and tools must have clear, comprehensive
  documentation that explains their purpose, limitations, and usage. Documentation
  should use terminology that users can understand, provide helpful guidance for common
  scenarios, and include warnings about potential issues.
repository: google-gemini/gemini-cli
label: Documentation
language: TypeScript
comments_count: 6
repository_stars: 65062
---

All user-facing features, APIs, and tools must have clear, comprehensive documentation that explains their purpose, limitations, and usage. Documentation should use terminology that users can understand, provide helpful guidance for common scenarios, and include warnings about potential issues.

Key requirements:
- Clearly document scope and limitations (e.g., "scoped only to md files")
- Provide usage guidance and examples for complex features
- Use clear, specific language instead of technical jargon
- Include helpful messages and warnings for error cases
- Ensure all commands and tools have descriptions
- Explain what information is being provided to users

Example of good documentation:
```typescript
/**
 * Processes import statements in GEMINI.md content
 * Supports @path/to/file.md syntax for importing content from other files
 * 
 * Note: Only .md files are supported. Attempting to import other file types
 * will result in a warning and the import will be skipped.
 */
export async function processImports(content: string, basePath: string): Promise<string> {
  // Implementation with clear error messages for unsupported file types
  if (!importPath.endsWith('.md')) {
    console.warn(`[WARN] Only .md files are supported for imports. Skipping: ${importPath}`);
    return content;
  }
}
```

This ensures users can effectively use features without confusion and reduces support burden by providing clear guidance upfront.