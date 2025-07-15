---
title: Clear accurate documentation
description: Documentation should be both technically accurate and contextually helpful
  for developers. Comments and JSDoc entries must correctly describe the behavior,
  purpose, and relationships of code elements.
repository: oven-sh/bun
label: Documentation
language: TypeScript
comments_count: 4
repository_stars: 79093
---

Documentation should be both technically accurate and contextually helpful for developers. Comments and JSDoc entries must correctly describe the behavior, purpose, and relationships of code elements.

Key practices:
- Ensure documentation accurately describes what code does, not just what it is
- Make comments contextually relevant, explaining the "why" behind implementation details
- Use fully-qualified type names in references (e.g., `Bun.BodyInit` instead of just `BodyInit`)
- Be specific about requirements and relationships between code components

**Examples:**

Instead of vague comments:
```ts
// keep this in sync with src/bun.js/bindings/webcore/JSReadableStream.cpp customInspect
// keep this in sync with src/bun.js/bindings/webcore/JSWritableStream.cpp customInspect
```

Use explanatory comments that convey purpose:
```ts
// These must match the order of the stateNames arrays in JSReadableStream.cpp and JSWritableStream.cpp
```

Instead of imprecise JSDoc:
```ts
/**
 * Local IP address connected to the socket
 * @example "192.168.1.100" | "2001:db8::1"
 */
readonly localFamily: string;
```

Use technically accurate descriptions:
```ts
/**
 * IP protocol family used for the local endpoint of the socket
 * @example "IPv4" | "IPv6"
 */
readonly localFamily: string;
```