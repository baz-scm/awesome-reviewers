---
title: Maintain API compatibility
description: When modifying existing APIs, ensure backward compatibility to prevent
  runtime failures and minimize migration effort for consumers. Breaking changes in
  function signatures, return types, or parameter requirements can cause cascading
  issues throughout a codebase.
repository: continuedev/continue
label: API
language: TypeScript
comments_count: 4
repository_stars: 27819
---

When modifying existing APIs, ensure backward compatibility to prevent runtime failures and minimize migration effort for consumers. Breaking changes in function signatures, return types, or parameter requirements can cause cascading issues throughout a codebase.

Follow these practices for API evolution:

1. **Use optional parameters for new functionality** instead of adding required parameters. This allows existing code to continue working without modification.

```typescript
// Bad: Breaking change - adding a required parameter
- embed(chunks: string[]): Promise<number[][]>;
+ embed(chunks: string[], embedding_task: EmbeddingTasks): Promise<number[][]>;

// Good: Backward compatible change
+ embed(chunks: string[], embedding_task?: EmbeddingTasks): Promise<number[][]>;
```

2. **Preserve return type compatibility** by using interface extension rather than changing the return type structure.

```typescript
// Bad: Breaking return type change
- function compileChatMessages(...): ChatMessage[] {
+ function compileChatMessages(...): { compiledChatMessages: ChatMessage[]; lastMessageTruncated: boolean } {

// Good: Backward compatible approach
+ interface ChatMessagesResult {
+   messages: ChatMessage[];
+   lastMessageTruncated?: boolean;
+ }
+ function compileChatMessages(...): ChatMessagesResult {
```

3. **Use parameter objects** for functions likely to evolve, making it easier to add options without breaking changes.

```typescript
// Bad: Making previously optional parameters required
- required: ["name", "rule"],
+ required: ["name", "rule", "alwaysApply", "description"],

// Good: Keep core parameters required, make new ones optional
+ required: ["name", "rule"],
+ properties: {
+   alwaysApply: { type: "boolean", default: false },
+   description: { type: "string", default: "" },
+ }
```

4. **When breaking changes are unavoidable**, provide function overloads or migration utilities to ease the transition for API consumers.

Remember that every API change affects all dependent code. Taking the time to design evolution-friendly interfaces upfront prevents costly migrations later.