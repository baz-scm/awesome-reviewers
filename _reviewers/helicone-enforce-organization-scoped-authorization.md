---
title: Enforce organization-scoped authorization
description: Every endpoint, manager method, or database query that reads or mutates
  tenant data must explicitly verify and scope access to the authenticated user's
  organization — never rely solely on a client-supplied ID (e.g., a record's `id`)
  to locate a resource. Add `organization_id`/`organizationId` filters to every SELECT,
  UPDATE, and DELETE, and pass identifiers...
repository: Helicone/helicone
label: Security
language: TypeScript
comments_count: 6
repository_stars: 6248
---

Every endpoint, manager method, or database query that reads or mutates tenant data must explicitly verify and scope access to the authenticated user's organization — never rely solely on a client-supplied ID (e.g., a record's `id`) to locate a resource. Add `organization_id`/`organizationId` filters to every SELECT, UPDATE, and DELETE, and pass identifiers as bound parameters rather than interpolating them into raw SQL strings, to prevent both cross-tenant data leaks and injection attacks.

Example:
```ts
// Bad: no tenant scoping, vulnerable to cross-org access
await dbExecute(
  "UPDATE saved_queries SET name = $1, sql = $2 WHERE id = $3",
  [name, sql, id]
);

// Good: scoped to the authenticated org, using bound parameters
await dbExecute(
  "UPDATE saved_queries SET name = $1, sql = $2 WHERE id = $3 AND organization_id = $4",
  [name, sql, id, authParams.organizationId]
);
```

Additionally:
- Never expose endpoints that leak sensitive existence/state information (e.g., "does this email exist") that enable enumeration attacks; prefer generic responses and handle provisioning logic server-side.
- Any service account or internal client (e.g., a dedicated DB user) that can access broad or cross-org data must require strong credentials — never leave passwords empty just because the account is "internal."
- Simple input checks (like payload size limits) are not a substitute for real authorization. Pair such validations with proper RBAC/tier checks and rate limiting on sensitive operations (e.g., signed URL generation).

Treat every new query, controller, or manager method as a potential authorization gap by default, and require an explicit organization/tenant check and parameterized inputs before merging.</description>
