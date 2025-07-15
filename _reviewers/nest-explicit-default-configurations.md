---
title: Explicit default configurations
description: Always provide explicit default values for configuration options to improve
  code readability and maintainability. Use helper methods consistently for default
  value management, and document defaults clearly.
repository: nestjs/nest
label: Configurations
language: TypeScript
comments_count: 9
repository_stars: 71767
---

Always provide explicit default values for configuration options to improve code readability and maintainability. Use helper methods consistently for default value management, and document defaults clearly.

When setting configuration options:

1. Use helper methods like `getOptionsProp()` with explicit default values:
```typescript
// Good - default value is explicit
this.port = this.getOptionsProp(options, 'port', TCP_DEFAULT_PORT);
this.rawOutputPackets = this.getOptionsProp(options, 'rawOutputPackets', false);

// Avoid - implicit default through || operator
this.port = this.getOptionsProp(options, 'port') || TCP_DEFAULT_PORT;
```

2. Conditionally add configuration options only when needed:
```typescript
// Good - only add config when value exists
const serverOptions = {
  ...this.maxSendMessageLength ? 
    { 'grpc.max_send_message_length': this.maxSendMessageLength } : 
    {}
};

// Avoid - setting undefined values
const serverOptions = {
  'grpc.max_send_message_length': this.maxSendMessageLength
};
```

3. Document default values using appropriate JSDoc tags:
```typescript
/**
 * Defines if file parameter is optional.
 * @default false
 */
optional?: boolean;

// When defaults differ between contexts (e.g., client vs server):
/**
 * Defaults to `"-server"` on server side and `"-client"` on client side.
 */
clientId?: string;
```

4. Avoid duplicating default values that are already defined by dependencies. Instead, rely on the dependency's defaults unless you have a specific reason to override them.

Following these practices makes configuration behavior more predictable and self-documenting, reduces bugs from unexpected undefined values, and makes code easier to maintain.