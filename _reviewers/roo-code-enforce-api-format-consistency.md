---
title: Enforce API format consistency
description: 'Maintain consistent data formats, parameter units, and interface patterns
  across API implementations. This includes:


  1. Consistent type mappings and format handling'
repository: RooCodeInc/Roo-Code
label: API
language: TypeScript
comments_count: 6
repository_stars: 17288
---

Maintain consistent data formats, parameter units, and interface patterns across API implementations. This includes:

1. Consistent type mappings and format handling
2. Standardized parameter units and descriptions
3. Uniform message format processing

Example of problematic inconsistencies:

```typescript
// Inconsistent MIME type mapping
const mimeTypes: Record<string, string> = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    // Missing MIME type for supported format
    // .avif is in SUPPORTED_IMAGE_FORMATS but not mapped here
}

// Inconsistent parameter unit description
openAiApiTimeout: z.number().optional().describe("Timeout in milliseconds"),
// But actually handled as minutes in implementation:
const timeoutMs = (options.timeout ?? 10) * 60 * 1000

// Inconsistent message format handling
// Don't convert structured data to plain text when the API supports JSON
const args = [
    "-p",
    JSON.stringify(messages),  // Correct: Preserve message structure
    "--system-prompt",
    systemPrompt
]
```

To maintain consistency:
1. Document and implement complete type mappings for all supported formats
2. Use consistent units across parameter definitions and implementations
3. Preserve data structures when APIs support them natively
4. Document format requirements and conversions in interface definitions