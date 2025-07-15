---
title: Keep tests simple
description: 'Tests should be straightforward, explicit, and free from complex logic
  or indirection. Avoid "magic" in tests that makes them harder to understand at a
  glance. When designing tests:'
repository: vercel/ai
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 15590
---

Tests should be straightforward, explicit, and free from complex logic or indirection. Avoid "magic" in tests that makes them harder to understand at a glance. When designing tests:

1. Prefer explicit setup over helper functions that hide details:
```javascript
// Avoid:
const store = initStore(chats);

// Prefer:
const store = new ChatStore({ chats });
```

2. Inline test data directly rather than using complex extraction logic:
```javascript
// Avoid:
const text = content
  .filter(item => item.type === 'text' && !item.thought)
  .map(item => item.text)
  .join('');

// Prefer:
expect(content).toMatchInlineSnapshot(`
  [
    { "type": "text", "text": "Hello, World!" },
  ]
`);
```

3. Test one behavior per test case so they can fail independently and provide clear signals about what's broken.

4. Make tests deterministic by stubbing variable elements like dates, timeouts, and IDs.

Simple tests are easier to understand, debug, and maintain, serving effectively as both verification tools and living documentation of expected behavior.