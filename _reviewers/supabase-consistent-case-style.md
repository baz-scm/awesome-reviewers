---
title: Consistent case style
description: Use consistent case styles in your codebase, adapting to the conventions
  of the ecosystem you're interacting with. When working with systems that use snake_case
  (like many Python-based backends, databases, or MCP servers), maintain that convention
  in your interfaces to those systems.
repository: supabase/supabase
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 86070
---

Use consistent case styles in your codebase, adapting to the conventions of the ecosystem you're interacting with. When working with systems that use snake_case (like many Python-based backends, databases, or MCP servers), maintain that convention in your interfaces to those systems.

Benefits:
- Improves code readability and maintainability
- Creates consistency across ecosystem boundaries
- Can improve performance with ML models that are trained predominantly on certain syntactic patterns

**Example:**
```typescript
// Good: Using snake_case for fields that interface with a snake_case system
const logFields = {
  log_type: 'postgres',
  event_message: message,
  api_role: role
};

// Not recommended: Mixing conventions when interfacing with snake_case systems
const logFields = {
  logType: 'postgres',  // camelCase
  event_message: message,  // snake_case
  apiRole: role  // camelCase
};
```

For new components, consider the primary systems they'll interact with and adopt the prevailing convention. Document your case style decisions in your team's style guide to maintain consistency.