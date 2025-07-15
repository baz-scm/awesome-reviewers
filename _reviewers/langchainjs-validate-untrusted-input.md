---
title: Validate untrusted input
description: Always validate and sanitize user-provided inputs before using them in
  sensitive contexts like SQL queries, file paths, or URL requests. This prevents
  SQL injection, path traversal, SSRF, and similar attacks.
repository: langchain-ai/langchainjs
label: Security
language: TypeScript
comments_count: 5
repository_stars: 15004
---

Always validate and sanitize user-provided inputs before using them in sensitive contexts like SQL queries, file paths, or URL requests. This prevents SQL injection, path traversal, SSRF, and similar attacks.

For SQL queries, use parameterized queries instead of string concatenation:

```typescript
// UNSAFE - vulnerable to SQL injection:
const query = `SELECT column_name FROM information_schema.columns WHERE table_name = '${tableName}'`;

// SAFE - using parameterized queries:
const query = `SELECT column_name FROM information_schema.columns WHERE table_name = ?`;
await connection.execute(query, [tableName]);
```

For file paths, validate against directory traversal attempts:

```typescript
// Validate that paths don't try to escape the intended directory
if (path.includes('..') || path.startsWith('/') || path.includes('\\')) {
  throw new Error("Invalid path: directory traversal attempt detected");
}
```

For URL requests, implement validation and consider using allowlists:

```typescript
function isValidUrl(url: string): boolean {
  try {
    const parsedUrl = new URL(url);
    // Check against allowlist of domains or protocols
    return ['https:'].includes(parsedUrl.protocol) && 
           ALLOWED_DOMAINS.includes(parsedUrl.hostname);
  } catch {
    return false;
  }
}

if (!isValidUrl(userProvidedUrl)) {
  throw new Error("Invalid or disallowed URL");
}
```

When developing API endpoints or libraries, clearly document in JSDoc comments which parameters must come from trusted sources and cannot accept direct user input.
