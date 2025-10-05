---
title: Serialize dynamic code inputs
description: Always serialize or sanitize user-controlled data before embedding it
  in dynamically generated code to prevent code injection vulnerabilities. Unsanitized
  inputs containing special characters like quotes can break JavaScript syntax or
  enable malicious code execution.
repository: TanStack/router
label: Security
language: TypeScript
comments_count: 1
repository_stars: 11590
---

Always serialize or sanitize user-controlled data before embedding it in dynamically generated code to prevent code injection vulnerabilities. Unsanitized inputs containing special characters like quotes can break JavaScript syntax or enable malicious code execution.

When injecting values into generated JavaScript, use proper serialization methods rather than direct string concatenation:

```typescript
// Vulnerable - direct injection without serialization
this.injectScript(`__TSR__.streamedValues['${key}'] = { value: ${value}}`)

// Secure - serialize inputs before injection  
this.injectScript(`__TSR__.streamedValues.push([${this.serializer?.(key)}, ${this.serializer?.(value)}])`)
```

This applies to any scenario where user input is embedded in generated code, including SQL queries, HTML templates, JavaScript snippets, and configuration files. Use appropriate escaping or serialization functions for the target context to maintain both functionality and security.