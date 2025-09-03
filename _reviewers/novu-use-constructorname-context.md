---
title: Use constructor.name context
description: Always set logger context using `this.constructor.name` and configure
  it via the `setContext()` method rather than hardcoding context strings or passing
  context as parameters to individual log calls.
repository: novuhq/novu
label: Logging
language: TypeScript
comments_count: 2
repository_stars: 37700
---

Always set logger context using `this.constructor.name` and configure it via the `setContext()` method rather than hardcoding context strings or passing context as parameters to individual log calls.

This approach ensures consistency across the codebase and proper context display in logs. Hardcoded context strings can become outdated when classes are renamed, while `this.constructor.name` automatically reflects the current class name.

**Correct approach:**
```typescript
@Injectable()
export class SendWebhookMessage {
  constructor(private logger: PinoLogger) {
    this.logger.setContext(this.constructor.name);
  }

  async execute() {
    // Context is already set, no need to pass it
    this.logger.error({ err: error }, 'Failed to create execution details');
  }
}
```

**Avoid:**
```typescript
// Don't use hardcoded context strings
const LOG_CONTEXT = 'SendWebhookMessageUseCase';
this.logger.setContext(LOG_CONTEXT);

// Don't pass context as parameter - it won't be used properly
this.logger.error({ err: error }, 'Failed to create execution details', LOG_CONTEXT);
```

Setting context once in the constructor ensures all log messages from that class instance include the proper context automatically, making logs more traceable and maintainable.