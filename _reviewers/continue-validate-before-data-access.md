---
title: Validate before data access
description: 'Always validate data existence and type before accessing properties
  or methods to prevent runtime errors from null/undefined values. This includes:


  1. Array bounds checking before indexing'
repository: continuedev/continue
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 27819
---

Always validate data existence and type before accessing properties or methods to prevent runtime errors from null/undefined values. This includes:

1. Array bounds checking before indexing
2. Object property existence verification
3. Type validation before method calls
4. Use of optional chaining and nullish coalescing operators

Example of unsafe code:
```typescript
function toolCallStateToSystemToolCall(state: ToolCallState): string {
  return state.toolCall.function.name;  // Unsafe - multiple potential null points
}
```

Safe version:
```typescript
function toolCallStateToSystemToolCall(state: ToolCallState): string {
  if (!state?.toolCall?.function) {
    throw new Error("Invalid tool call state");
  }
  return state.toolCall.function.name ?? "unknown";
}
```

Key practices:
- Use optional chaining (?.) for nested object access
- Provide default values using nullish coalescing (??)
- Add explicit null checks for critical operations
- Validate array indices before access
- Check object type and property existence before destructuring

This prevents the most common causes of runtime errors and improves code reliability.