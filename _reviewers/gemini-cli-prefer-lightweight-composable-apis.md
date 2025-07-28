---
title: Prefer lightweight composable APIs
description: When designing APIs, favor lightweight, composable solutions that allow
  callers to maintain control over their specific use cases, rather than imposing
  centralized, monolithic systems that take control away from the caller.
repository: google-gemini/gemini-cli
label: API
language: Markdown
comments_count: 2
repository_stars: 65062
---

When designing APIs, favor lightweight, composable solutions that allow callers to maintain control over their specific use cases, rather than imposing centralized, monolithic systems that take control away from the caller.

This principle emerges from recognizing that different parts of an application often have unique requirements that are difficult to accommodate in a one-size-fits-all solution. Lightweight APIs that provide building blocks for callers to compose are more flexible and easier to adopt incrementally.

For example, instead of creating a centralized service that "requires taking control of all useInput in the application," design an API that "allows callers to resolve whether specific input matches a specific keybinding." This approach respects existing code patterns and reduces the risk of breaking changes during adoption.

Similarly, when handling user input or arguments, prefer simple, predictable approaches like direct appending rather than complex parsing mechanisms with special separators. This makes the API more intuitive and reduces cognitive overhead for both implementers and users.

```javascript
// Avoid: Centralized control that requires major refactoring
const keybindingService = new KeybindingService();
keybindingService.takeControlOfAllInput();

// Prefer: Composable utilities that work with existing patterns
const isMatch = keybindingResolver.matches(input, 'save-file');
if (isMatch) handleSave();
```