---
title: Use structured logging consistently
description: Always use the established logging framework instead of console.log or
  ad-hoc logging approaches. This ensures consistent log formatting, proper log levels,
  and better log management across the application.
repository: browserbase/stagehand
label: Logging
language: TypeScript
comments_count: 5
repository_stars: 16443
---

Always use the established logging framework instead of console.log or ad-hoc logging approaches. This ensures consistent log formatting, proper log levels, and better log management across the application.

When logging errors, include contextual information like error traces, messages, and auxiliary data to make logs more informative for debugging. For components that need logging capabilities, inherit or inject the logger from the main application rather than creating separate logging mechanisms.

Example of what to avoid:
```typescript
console.log(options.messages);
console.log(tree);
```

Example of proper structured logging:
```typescript
this.logger({
  category: "debug",
  message: "Processing options messages",
  auxiliary: { messageCount: options.messages.length }
});

this.stagehandLogger.error(
  "The browser context is undefined. This means the CDP connection to the browser failed"
);
```

This approach provides better log filtering, formatting, and integration with log management systems while maintaining consistency across the codebase.