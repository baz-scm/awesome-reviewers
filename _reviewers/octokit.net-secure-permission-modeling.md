---
title: Secure permission modeling
description: 'When implementing security-related models such as permissions, carefully
  design the properties to prevent unauthorized modifications and maintain appropriate
  constraints:'
repository: octokit/octokit.net
label: Security
language: C#
comments_count: 2
repository_stars: 2793
---

When implementing security-related models such as permissions, carefully design the properties to prevent unauthorized modifications and maintain appropriate constraints:

1. Make security-sensitive properties immutable where possible using read-only properties or private setters:
```csharp
// Preferred
public bool Admin { get; }
// Or
public bool Admin { get; private set; }

// Avoid
public bool Admin { get; protected set; }
// Never
public bool Admin { get; set; }
```

2. When modeling permission values, consider the tradeoff between type safety and flexibility:
   - Use enums (StringEnum<PermissionLevel>) when values are strictly defined and limited
   - Use strings only when necessary (e.g., for custom roles in enterprise systems)
   - Document the rationale when moving from constrained types to more flexible ones

3. When expanding permission models, ensure backward compatibility while maintaining security guarantees.

Proper permission modeling reduces the risk of security vulnerabilities by preventing unintended permission modifications and providing compile-time safety where appropriate.