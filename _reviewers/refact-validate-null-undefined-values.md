---
title: validate null undefined values
description: Always perform explicit null and undefined checks before accessing object
  properties or using values in operations. Filter out undefined values from arrays
  and collections to prevent runtime errors and unexpected behavior.
repository: smallcloudai/refact
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 3114
---

Always perform explicit null and undefined checks before accessing object properties or using values in operations. Filter out undefined values from arrays and collections to prevent runtime errors and unexpected behavior.

Key practices:
- Keep null checks even when they seem redundant (`typeof value === "object" && value !== null`)
- Use property existence checks before accessing nested properties (`"tool_call_id" in msg`)
- Filter undefined values from arrays to maintain data integrity
- Validate object properties exist before comparison operations

Example:
```typescript
// Good: Explicit null check prevents runtime errors
if (typeof value === "object" && value !== null) {
  // Safe to access properties
}

// Good: Check property existence and filter undefined values
const toolMessages = tailMessages
  .filter(msg => "tool_call_id" in msg)
  .map(msg => msg.tool_call_id)
  .filter(id => id !== undefined);

// Good: Validate before property access
if (maybeLastAssistantMessageUsage) {
  const allMatch = Object.entries(currentUsage).every(
    ([key, value]) => maybeLastAssistantMessageUsage[key] === value
  );
}
```