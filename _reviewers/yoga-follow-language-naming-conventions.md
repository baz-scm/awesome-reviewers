---
title: Follow language naming conventions
description: Ensure all identifiers (properties, methods, classes, variables) follow
  the established naming conventions of the programming language being used. This
  improves code readability, maintainability, and consistency across the codebase.
repository: facebook/yoga
label: Naming Conventions
language: C#
comments_count: 2
repository_stars: 18255
---

Ensure all identifiers (properties, methods, classes, variables) follow the established naming conventions of the programming language being used. This improves code readability, maintainability, and consistency across the codebase.

For example, in C#:
- Properties should use PascalCase: `MeasureOutput` instead of `measureOutput`
- Avoid platform-specific naming that reduces portability: use `"CSSLayout"` instead of `"CSSLayout.dll"`

Language conventions exist for good reasons - they make code more predictable for other developers familiar with the language, improve IDE support and tooling integration, and maintain consistency with standard libraries and frameworks. When naming conflicts arise, prioritize following the language's established patterns over personal preferences or porting convenience.