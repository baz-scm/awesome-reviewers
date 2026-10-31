---
title: RESTful endpoint and type design
description: 'Design API endpoints and their request/response types deliberately.
  Prefer RESTful resource-based routes over verb-based ones when the HTTP method already
  conveys the action (e.g., `POST /prompt-2025` instead of `POST /prompt-2025/create`).
  Keep response types precise and minimal: only include fields that are actually returned
  by a given endpoint,...'
repository: Helicone/helicone
label: API
language: TypeScript
comments_count: 3
repository_stars: 6248
---

Design API endpoints and their request/response types deliberately. Prefer RESTful resource-based routes over verb-based ones when the HTTP method already conveys the action (e.g., `POST /prompt-2025` instead of `POST /prompt-2025/create`). Keep response types precise and minimal: only include fields that are actually returned by a given endpoint, especially sensitive data. For example, if an API key is only meant to be surfaced once at creation time, don't include it on the shared type used by subsequent read/update responses—define it inline on the create response instead so the type signature matches real behavior and prevents accidental leakage. When request/response DTOs overlap (e.g., `CreateSavedQueryRequest` and `UpdateSavedQueryRequest`), avoid duplicating shared fields; extend a common base interface so future field changes stay in sync across related types:

```ts
export interface CreateSavedQueryRequest {
  name: string;
  sql: string;
}

export interface UpdateSavedQueryRequest extends CreateSavedQueryRequest {
  id: string;
}
```

Applying these practices keeps endpoints predictable, type definitions trustworthy, and reduces the risk of exposing or duplicating data incorrectly as the API evolves.