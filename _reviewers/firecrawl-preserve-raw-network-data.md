---
title: preserve raw network data
description: Always preserve raw network response data early in the processing pipeline
  before applying any transformations or parsing. Once network data is processed or
  encoded, critical information may be permanently lost and cannot be recovered later.
repository: firecrawl/firecrawl
label: Networking
language: TypeScript
comments_count: 2
repository_stars: 54535
---

Always preserve raw network response data early in the processing pipeline before applying any transformations or parsing. Once network data is processed or encoded, critical information may be permanently lost and cannot be recovered later.

This is particularly important for:
- Character encoding detection and conversion (handle at buffer level, not string level)
- HTML parsing where raw content may contain links or metadata not preserved in cleaned versions
- Any data transformation that might be lossy or irreversible

Example of the problem:
```typescript
// BAD: Encoding conversion after string processing
function encodeRawHTML(document: Document): Document {
  // At this point, UTF-8 misencoding is "too destructive" 
  // to recover original Shift_JIS content
  const decoder = new TextDecoder(charset);
  document.rawHtml = decoder.decode(stringData); // Information already lost
}

// BAD: Using processed HTML for link extraction
linksOnPage = extractLinks(html, urlToScrap); // May miss links from raw content
```

Move encoding and parsing operations to earlier parts of the stack where you still have access to the raw network buffers. This prevents permanent data loss and ensures all network content is available for processing.