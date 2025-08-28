---
title: HTTP protocol compliance
description: Ensure HTTP protocol implementations strictly follow RFC standards and
  handle edge cases correctly. This includes proper header parsing that respects quoted-string
  constructions, realistic port value assignments, and appropriate status code filtering.
repository: cloudflare/workerd
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 6989
---

Ensure HTTP protocol implementations strictly follow RFC standards and handle edge cases correctly. This includes proper header parsing that respects quoted-string constructions, realistic port value assignments, and appropriate status code filtering.

Key areas to verify:

1. **Header parsing**: Avoid naive string splitting for headers that may contain quoted strings with commas. Headers like `content-type` and `authorization` can include quoted parameters that contain commas, requiring RFC 7230-compliant parsing that handles optional whitespace (OWS) and quoted-string constructions.

2. **Port value realism**: Use realistic port numbers for network simulation. Ephemeral source ports should be in the range 32768-65535 (2^15 to 2^16), not standard service ports like 80.

3. **Status code support**: Filter out unsupported HTTP status codes early in the implementation. For example, if 1xx status codes aren't supported by the runtime, validate and reject them at the protocol level.

4. **Node.js compatibility**: Support standard Node.js networking behaviors like automatic port assignment (port 0) where the system assigns an available port.

Example of problematic header parsing:
```typescript
// Incorrect - breaks on quoted strings
headers.push(key, value.split(', ').at(0) as string);

// Better approach needed for headers like:
// content-type: text/plain; f="a, b, c", text/foo; a="1, 2, 3"
```

Example of realistic port assignment:
```typescript
// Instead of hardcoded 80
get remotePort(): number {
  return 80; // Unrealistic for source ports
}

// Use realistic ephemeral port range
get remotePort(): number {
  return 32768; // Realistic source port
}
```

This ensures network protocol implementations are robust, standards-compliant, and handle real-world edge cases that could cause parsing failures or compatibility issues.