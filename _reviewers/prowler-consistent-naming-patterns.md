---
title: Consistent naming patterns
description: 'Follow systematic naming conventions for types, interfaces, and functions
  to enhance code readability and navigability:


  ### Type/Interface Naming

  - `*Data`: Full API models with `id`, `type`, `attributes`, `relationships` (e.g.,
  `RoleData`)'
repository: prowler-cloud/prowler
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 11834
---

Follow systematic naming conventions for types, interfaces, and functions to enhance code readability and navigability:

### Type/Interface Naming
- `*Data`: Full API models with `id`, `type`, `attributes`, `relationships` (e.g., `RoleData`)
- `*Attributes`: Only the attributes section of an object (e.g., `RoleAttributes`)
- `*Props`: React component props (e.g., `UserInfoProps`)
- `*FormValues`, `*Params`: Form schemas or context-specific helper types

### Function Naming
- Start with action verb (e.g., `get`, `create`)
- Follow with domain/feature name and resource
- Place adjectives before nouns (e.g., `getLatestFindings` not `getFindingsLatest`)

### Use Typed Constants
- Prefer enums over string literals for keys and constants

```typescript
// ❌ Avoid
interface Role { id: string; type: "roles"; attributes: { /* ... */ }; }
const getFindingsLatest = async () => { /* ... */ };
type CredentialsForm = { aws_access_key_id: string; /* string literals */ };

// ✅ Better
interface RoleData { id: string; type: "roles"; attributes: RoleAttributes; }
interface RoleAttributes { /* ... */ }
const getLatestFindings = async () => { /* ... */ };
enum CredentialKeys { AwsAccessKey = "aws_access_key_id" /* ... */ }
```

This systematic naming makes the code more self-documenting and helps developers quickly distinguish between different types of interfaces when reading or searching through the codebase.