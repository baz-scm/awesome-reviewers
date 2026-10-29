---
title: Semantic and consistent naming
description: Choose identifiers that accurately reflect what they represent and stay
  consistent with established project or architectural conventions. Avoid names that
  mislead about scope, purpose, or type.
repository: expressjs/Express
label: Naming Conventions
language: JavaScript
comments_count: 5
repository_stars: 69579
---

Choose identifiers that accurately reflect what they represent and stay consistent with established project or architectural conventions. Avoid names that mislead about scope, purpose, or type.

Specifically:
- Variable names should match their actual semantic role, not an earlier/narrower intent. For example, if a parameter can hold any value (not just an object), name it `val` rather than `obj` throughout its usage.
- When referencing the module/package itself (e.g., in `deprecate()` calls), use the actual npm package name rather than a submodule or internal name, so messages are meaningful to consumers.
- Follow established architectural naming patterns (e.g., Controller-Service-Repository) so classes and parameters are immediately recognizable by their role, such as naming a use-case/service class `NotesService` instead of a generic `NotesUseCase` when the project follows that convention.
- Clearly distinguish internal/private members from public API by using a leading underscore (e.g., `_router`) or another consistent convention, and never reuse the same name for a public property and an internal one with different semantics (e.g., don't have both a public `app.router` method and an internal `_router` property that serve different purposes under confusingly similar names).

Applying these rules keeps code self-documenting, reduces ambiguity about visibility/intent, and prevents subtle bugs or confusion caused by names that no longer match their actual usage.