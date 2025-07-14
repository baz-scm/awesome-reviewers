---
title: Follow consistent naming patterns
description: 'Maintain consistent naming conventions throughout the codebase to improve
  readability and reduce confusion. Adhere to these guidelines:


  1. **Function naming patterns**: Use established prefixes like `create` for factory
  functions, which accurately conveys their purpose and aligns with existing patterns.'
repository: nodejs/node
label: Naming Conventions
language: Markdown
comments_count: 5
repository_stars: 112178
---

Maintain consistent naming conventions throughout the codebase to improve readability and reduce confusion. Adhere to these guidelines:

1. **Function naming patterns**: Use established prefixes like `create` for factory functions, which accurately conveys their purpose and aligns with existing patterns.
   ```js
   // Preferred
   const counter = createCounter('api.calls', { service: 'web' });
   const timer = createTimer('api.request.duration', { service: 'web' });
   
   // Avoid
   const counter = counter('api.calls', { service: 'web' });
   ```

2. **Method capitalization**: Document instance methods with lowercase first letters, reserving capitalization for static methods.
   ```js
   // Preferred (instance method)
   blockList.fromJSON(value)
   
   // Avoid (incorrect capitalization for instance method)
   BlockList.fromJSON(value)
   ```
   
3. **Semantic specificity**: Choose specific method names that prevent collisions and clearly communicate purpose. Avoid overly generic names like `use()` when more descriptive alternatives like `useEventListener()` or `addDisposableEventListener()` are clearer.

4. **Domain-consistent terminology**: Use consistent terminology across related APIs. For example, if most of your file system API uses "file descriptor" or "fd", maintain that terminology throughout rather than using alternatives like "handle" for the same concept.

5. **Documentation formatting**: Follow established documentation patterns. Don't introduce formatting inconsistencies like prefixing types with "Type:" when the rest of the documentation uses a different convention.

Consistent naming makes codebases easier to learn, navigate, and maintain while reducing cognitive load for developers.