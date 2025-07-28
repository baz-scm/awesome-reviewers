---
title: Use backticks for identifiers
description: Wrap all code identifiers, method names, interface names, class names,
  and API references in JSDoc comments with backticks (`) for proper monospacing and
  improved readability.
repository: denoland/deno
label: Documentation
language: TypeScript
comments_count: 3
repository_stars: 103714
---

Wrap all code identifiers, method names, interface names, class names, and API references in JSDoc comments with backticks (`) for proper monospacing and improved readability.

This includes:
- Interface and class names (e.g., `EventTarget`, `EventListener`)
- Method names (e.g., `addEventListener()`, `handleEvent()`)
- Property names and parameter names
- API references and technical terms

**Example:**
```typescript
/**
 * The `EventListenerObject` interface represents an object that can handle events
 * dispatched by an `EventTarget` object.
 *
 * This interface provides an alternative to using a function as an event listener.
 * When implementing an object with this interface, the `handleEvent()` method
 * will be called when the event is triggered.
 */
interface EventListenerObject {
  handleEvent(evt: Event): void;
}
```

**Instead of:**
```typescript
/**
 * The EventListenerObject interface represents an object that can handle events
 * dispatched by an EventTarget object.
 *
 * When implementing an object with this interface, the handleEvent() method
 * will be called when the event is triggered.
 */
```

This formatting convention ensures consistent documentation styling, improves code readability in generated documentation, and follows standard JSDoc best practices for technical documentation.