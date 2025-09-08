---
title: Environment-specific configuration identifiers
description: Use distinct, environment-specific identifiers in configuration to prevent
  conflicts between different application contexts (development vs production, different
  versions, etc.) and ensure semantic clarity.
repository: gravitational/teleport
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 19109
---

Use distinct, environment-specific identifiers in configuration to prevent conflicts between different application contexts (development vs production, different versions, etc.) and ensure semantic clarity.

When configuration values like IDs, state names, or identifiers could be ambiguous or cause conflicts across environments, make them explicitly environment-aware and semantically meaningful.

Examples:
- Instead of a single hardcoded GUID for tray icons, use different GUIDs for dev vs packaged versions to prevent conflicts when running multiple instances
- Instead of generic state names like `isHidden` that could be ambiguous, use semantically clear names like `isInBackgroundMode` that explicitly convey the intended behavior and context

This prevents runtime conflicts, reduces debugging complexity, and makes the codebase more maintainable by eliminating ambiguity about configuration intent and scope.