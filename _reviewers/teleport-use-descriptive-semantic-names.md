---
title: Use descriptive semantic names
description: Choose descriptive, semantic names that clearly convey purpose and meaning
  rather than generic or ambiguous identifiers. Avoid generic method names like `apply`
  or `handle` that don't indicate their specific function. When existing semantic
  references are available (such as theme palette names), prefer them over hardcoded
  values. Add clarifying comments...
repository: gravitational/teleport
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 19109
---

Choose descriptive, semantic names that clearly convey purpose and meaning rather than generic or ambiguous identifiers. Avoid generic method names like `apply` or `handle` that don't indicate their specific function. When existing semantic references are available (such as theme palette names), prefer them over hardcoded values. Add clarifying comments when names might be ambiguous or when distinguishing between similar concepts.

Examples:
- Instead of generic method names: `apply()` → `applyTtyEvent()` or `handleTerminalResize()`
- Use existing semantic references: `background: 'black'` → `background: interactive.tonal.neutral.background`
- Add clarifying comments for similar names:
```ts
ApplicationAwsCliConsole = 'application-aws-cli-console', // AWS OIDC IdP
ApplicationAwsRolesAnywhere = 'application-aws-iam-roles-anywhere',
```

This practice improves code readability, reduces cognitive load, and makes the codebase more maintainable by making intent explicit.