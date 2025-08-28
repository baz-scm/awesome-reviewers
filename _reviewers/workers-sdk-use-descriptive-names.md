---
title: Use descriptive names
description: Choose names that clearly describe their purpose, behavior, and data
  type rather than generic or ambiguous alternatives. Function names should reflect
  what they actually do, variables should indicate their specific role, and parameter
  names should convey semantic meaning.
repository: cloudflare/workers-sdk
label: Naming Conventions
language: TypeScript
comments_count: 8
repository_stars: 3379
---

Choose names that clearly describe their purpose, behavior, and data type rather than generic or ambiguous alternatives. Function names should reflect what they actually do, variables should indicate their specific role, and parameter names should convey semantic meaning.

**Key principles:**
- **Functions**: Name based on actual behavior, not outdated descriptions
- **Variables**: Use specific, descriptive terms over generic ones  
- **Parameters**: Prefer named object parameters over positional booleans for clarity
- **Types**: Avoid names that suggest incorrect data types

**Examples:**

```typescript
// ❌ Generic/misleading names
function deserializeToJson(message) { return JSON.parse(message.toString()); }
const directory = "/path/to/project";
const pinFrameworkCli = "1.2.3"; // suggests boolean
updateTsConfig(ctx, true); // unclear what true means

// ✅ Descriptive names  
function deserializeJson(message) { return JSON.parse(message.toString()); }
const projectRoot = "/path/to/project";
const frameworkCliPinnedVersion = "1.2.3";
updateTsConfig(ctx, { usesNodeCompat: true });
```

This approach reduces cognitive load, prevents misunderstandings about data types and behavior, and makes code self-documenting. When reviewing code, ask: "Does this name clearly communicate what this thing is or does?"