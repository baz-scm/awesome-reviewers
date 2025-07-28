---
title: API consistency patterns
description: Maintain consistent interface patterns across APIs and avoid loose coupling
  through magic strings or unstable properties. APIs should follow established conventions
  and provide stable, well-defined contracts.
repository: google-gemini/gemini-cli
label: API
language: TypeScript
comments_count: 5
repository_stars: 65062
---

Maintain consistent interface patterns across APIs and avoid loose coupling through magic strings or unstable properties. APIs should follow established conventions and provide stable, well-defined contracts.

Key principles:
1. **Follow established patterns**: When designing new APIs, align with existing SDK patterns and conventions. For example, subagent interfaces should "keep this interface consistent with what you see if you are using the SDKs natively" by using standard system prompt strings and chat pairs.

2. **Avoid magic strings and loose metadata**: Don't rely on consumers knowing magic strings or loose information. Instead of metadata objects with string-based properties, use strongly-typed enums or explicit properties that provide compile-time safety.

3. **Use stable properties**: Prefer stable, well-defined properties over transient values. For instance, use `schema` (a stable BaseTool property) rather than `parameterSchema` (a transient value used to populate the schema field).

4. **Standardize protocols**: Extract common protocol patterns into shared libraries rather than having integrators hardcode protocol layers. Methods like `ide/diffClosed` should be part of a protocol library that IDE integrations can import.

Example of good API consistency:
```typescript
// Good: Stable, consistent interface
interface ToolInterface {
  name: string;
  schema: SchemaUnion; // Stable property
  execute(params: ToolParams): Promise<ToolResult>;
}

// Avoid: Loose coupling with magic strings
interface ToolInterface {
  metadata: { source: string; behavior: string }; // Magic strings
  parameterSchema: SchemaUnion; // Transient property
}
```

This approach ensures APIs are predictable, maintainable, and provide clear contracts for consumers.