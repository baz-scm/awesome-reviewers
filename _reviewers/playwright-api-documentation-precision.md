---
title: API documentation precision
description: API documentation must use specific, well-defined types instead of generic
  ones, and clearly define behavior for all scenarios including edge cases. When documenting
  return types, use explicit union types or named type aliases rather than generic
  strings. For complex APIs with multiple options, document the interaction between
  different parameters and their...
repository: microsoft/playwright
label: API
language: Markdown
comments_count: 2
repository_stars: 76113
---

API documentation must use specific, well-defined types instead of generic ones, and clearly define behavior for all scenarios including edge cases. When documenting return types, use explicit union types or named type aliases rather than generic strings. For complex APIs with multiple options, document the interaction between different parameters and their expected behavior.

For example, instead of:
```
- returns: <[string]>
```

Use specific union types:
```
- returns: <["log"|"debug"|"info"|"error"|"warning"|"dir"|"dirxml"|"table"|"trace"|"clear"|"startGroup"|"startGroupCollapsed"|"endGroup"|"assert"|"profile"|"profileEnd"|"count"|"timeEnd"]>
```

Or better yet, use named types:
```
- returns: <[ConsoleMessageType]>
```

Additionally, when introducing new API options, clearly document their behavior in all scenarios, especially when combined with other options or in edge cases. This prevents ambiguity and improves developer experience by making API contracts explicit and predictable.