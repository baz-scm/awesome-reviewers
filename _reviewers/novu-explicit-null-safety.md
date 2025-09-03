---
title: explicit null safety
description: Always perform explicit null and undefined checks before processing values,
  and use the nullish coalescing operator (??) for safe default value assignment.
  Distinguish between null (explicit no value) and undefined (use default) semantics
  in your API design.
repository: novuhq/novu
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 37700
---

Always perform explicit null and undefined checks before processing values, and use the nullish coalescing operator (??) for safe default value assignment. Distinguish between null (explicit no value) and undefined (use default) semantics in your API design.

When providing default values, prefer nullish coalescing over logical OR to avoid falsy value issues:

```typescript
// Good: Uses nullish coalescing for defaults
const severity = options.severity ?? SeverityLevelEnum.NONE;
const subscriberId = subscriber?.subscriberId ?? '';
const timezone = subscriber?.timezone ?? currentTimezone;

// Good: Explicit undefined check
if (typeof command.layoutIdOrInternalId === 'undefined') {
  // Use default layout
}

// Good: Explicit null check in sensitive code
if (!this.svix) {
  throw new BadRequestException('Webhook system is not enabled');
}

// Good: Handle null vs undefined semantics
// null = user explicitly wants no layout
// undefined = use default layout
layoutId: z.string().nullable().optional()

// Good: Explicit null check for string conversion
return value == null ? '' : String(value);
```

This pattern prevents null reference errors, makes default value logic clear, and ensures consistent behavior across null and undefined scenarios. Always validate these checks in sensitive code paths where null values could cause runtime failures.