---
title: Clear API interfaces
description: Ensure API interfaces are clearly defined with proper formatting and
  comprehensive documentation. Type definitions should use consistent formatting with
  appropriate line breaks for complex objects, and documentation should precisely
  explain callback behavior, timing, and parameters.
repository: vadimdemedes/ink
label: API
language: TypeScript
comments_count: 2
repository_stars: 31825
---

Ensure API interfaces are clearly defined with proper formatting and comprehensive documentation. Type definitions should use consistent formatting with appropriate line breaks for complex objects, and documentation should precisely explain callback behavior, timing, and parameters.

For type definitions, format complex objects with proper indentation:
```typescript
const renderToString: (
	node: ReactNode,
	options?: {
		columns?: number
	}
) => string;
```

For API documentation, be specific about when and how callbacks are invoked:
```typescript
/**
 * Hook that calls the `inputHandler` callback with the input that the program received.
 * Called on each keypress and when text is pasted.
 */
```

This ensures APIs are self-documenting and reduces confusion about interface contracts and expected behavior.