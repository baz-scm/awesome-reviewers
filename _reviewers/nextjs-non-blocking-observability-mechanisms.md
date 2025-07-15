---
title: "Non-blocking observability mechanisms"
description: "When implementing observability mechanisms like telemetry or status monitoring, ensure they don't block or interfere with critical application operations. Use background processes for telemetry submissions and dedicated endpoints for status checks."
repository: "vercel/next.js"
label: "Observability"
language: "TypeScript"
comments_count: 2
repository_stars: 133000
---

When implementing observability mechanisms like telemetry or status monitoring, ensure they don't block or interfere with critical application operations. Use background processes for telemetry submissions and dedicated endpoints for status checks.

For telemetry during shutdown operations:
```typescript
// Incorrect: Blocking on telemetry before shutdown
await telemetry.flush();
process.exit(RESTART_EXIT_CODE);

// Better: Use detached processes for telemetry
telemetry.flushDetached();
process.exit(RESTART_EXIT_CODE);
```

For service status monitoring:
```typescript
// Reliable approach: Query dedicated status endpoints
await fetchWithTimeout('/__nextjs_server_status');
// Then proceed with operations that may affect service

// Unreliable approach: Depending on functional endpoints that might be interrupted
await fetch('/__nextjs_restart_dev');
// Don't rely on response from endpoints that might be affected by the operation itself
```

This pattern ensures that observability data is collected reliably while maintaining system performance and responsiveness, particularly during critical lifecycle events like server restarts.