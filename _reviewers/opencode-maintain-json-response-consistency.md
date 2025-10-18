---
title: maintain JSON response consistency
description: When designing API responses that need to handle different data types
  or display states, maintain consistent JSON structure and use established encoding
  standards to preserve backward compatibility. Avoid changing response schemas that
  would break existing client integrations.
repository: sst/opencode
label: API
language: TypeScript
comments_count: 2
repository_stars: 28213
---

When designing API responses that need to handle different data types or display states, maintain consistent JSON structure and use established encoding standards to preserve backward compatibility. Avoid changing response schemas that would break existing client integrations.

For binary data in JSON responses, use base64 encoding as the standard approach:

```typescript
if (isBinary) {
  const buffer = await bunFile.arrayBuffer().catch(() => new ArrayBuffer(0))
  const content = Buffer.from(buffer).toString("base64")
  return { type: "binary", content, mimeType: getMimeType(full) }
}
```

For displaying modified or discounted values, use additional fields or metadata rather than changing the core data structure. This allows clients to handle the information appropriately while maintaining the expected response format. The principle follows established practices like AWS S3's JSON APIs, which use base64 encoding for binary content to ensure text-safe transmission within JSON payloads.