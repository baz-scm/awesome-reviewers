---
title: Document code meaningfully
description: 'Provide meaningful documentation that enhances code maintainability
  and understanding. Follow these practices:


  1. **Explain the "why"** - Document complex or non-obvious code behavior with comments
  that explain reasoning, not just functionality:'
repository: dotnet/runtime
label: Documentation
language: C#
comments_count: 5
repository_stars: 16578
---

Provide meaningful documentation that enhances code maintainability and understanding. Follow these practices:

1. **Explain the "why"** - Document complex or non-obvious code behavior with comments that explain reasoning, not just functionality:
```csharp
// Checking HasNewValue ensures the property setter is called even with null values,
// as setters may contain important initialization logic that should not be bypassed
if (bindingPoint.HasNewValue || bindingPoint.Value != null)
```

2. **Track TODOs properly** - Replace generic TODO comments with specific GitHub issue references:
```csharp
// TODO: Implement caching mechanism (see issue #1234)
```

3. **Attribute borrowed code** - When adapting code from external sources, include clear attribution with links and license information:
```csharp
// These definitions are derived from CDDL-licensed source code.
// Original source: https://src.illumos.org/source/xref/illumos-gate/usr/src/uts/common/sys/procfs.h
```

4. **Document APIs with XML comments** - Use XML documentation for public, internal, and significant private APIs to explain their purpose, parameters, and usage patterns, even for parameterless constructors that seed documentation.

5. **Keep documentation readable** - Ensure comments are concise, valuable, and formatted to avoid requiring horizontal scrolling.

Following these practices helps both current and future developers understand code intent, origin, and pending work, significantly reducing maintenance costs.
