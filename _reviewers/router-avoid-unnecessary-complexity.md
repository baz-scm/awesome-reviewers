---
title: avoid unnecessary complexity
description: Remove code complexity that doesn't provide clear value, particularly
  in type definitions, configuration options, and formatting constraints. This includes
  eliminating redundant type omissions, using descriptive names for configuration
  options, and avoiding formatting rules that conflict with user preferences.
repository: TanStack/router
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 11590
---

Remove code complexity that doesn't provide clear value, particularly in type definitions, configuration options, and formatting constraints. This includes eliminating redundant type omissions, using descriptive names for configuration options, and avoiding formatting rules that conflict with user preferences.

Examples of unnecessary complexity to avoid:
- Omitting types that get overwritten anyway: `Omit<ButtonProps, 'href'>` when `href` is replaced by the framework
- Generic configuration names: use `routeFileFormatter` instead of just `formatter` 
- Formatting constraints that assume specific code structure and conflict with user style preferences

The goal is to maintain clean, readable code without imposing arbitrary style restrictions or type gymnastics that don't serve a functional purpose. When in doubt, prefer simpler approaches that give users more control over their code style.