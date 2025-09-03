---
title: Implement graceful error fallbacks
description: Always implement fallback mechanisms when primary operations can fail,
  especially for critical operations like resource cleanup, async operations, and
  user-facing functionality. When the primary approach fails, provide a secondary
  method to handle the situation gracefully rather than letting errors propagate unchecked.
repository: menloresearch/jan
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 37620
---

Always implement fallback mechanisms when primary operations can fail, especially for critical operations like resource cleanup, async operations, and user-facing functionality. When the primary approach fails, provide a secondary method to handle the situation gracefully rather than letting errors propagate unchecked.

For resource cleanup, attempt graceful shutdown first, then force termination:
```typescript
function killSubprocess(): Promise<void> {
  return fetch(NITRO_HTTP_KILL_URL, {
    method: "DELETE",
  }).catch((err) => {
    console.error(err);
    subprocess.kill();
    subprocess = null;
    return kill(PORT, "tcp").then(console.log).catch(console.log);
  });
}
```

For user-facing operations, validate inputs and provide meaningful error handling:
```typescript
const convoId = currentConvo?.id
if (!convoId) {
  console.error('No conversation id')
  // TODO: Display toast notification to user
  return
}
```

This approach prevents silent failures, ensures resources are properly cleaned up even when primary methods fail, and maintains application stability by providing alternative paths when operations don't succeed as expected.