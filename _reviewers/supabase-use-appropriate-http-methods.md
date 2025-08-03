---
title: Use appropriate HTTP methods
description: Choose HTTP methods that align with the actual operation being performed.
  Use GET for retrieving data with query parameters, and POST for operations that
  modify state or require complex request bodies.
repository: supabase/supabase
label: API
language: TypeScript
comments_count: 2
repository_stars: 86070
---

Choose HTTP methods that align with the actual operation being performed. Use GET for retrieving data with query parameters, and POST for operations that modify state or require complex request bodies.

When designing API endpoints:

- For data retrieval operations, prefer GET requests with query parameters:
```typescript
// Better approach for data retrieval
const res = await fetchHandler(`${BASE_PATH}/api/check-cname?domain=${domain}`, {
  headers,
  method: 'GET'
});
```

- For operations with complex data requirements, use POST requests:
```typescript
const res = await fetchHandler(`${BASE_PATH}/api/resource`, {
  headers,
  method: 'POST',
  body: JSON.stringify(payload)
});
```

- Consider supporting both GET and POST methods for the same functionality when beneficial for client compatibility:
```typescript
if (req.method === 'GET') {
  const payload = { ...toForward, project_tier }
  return retrieveData(name as string, payload)
} else if (req.method === 'POST') {
  const payload = { ...req.body, project_tier }
  return retrieveData(name as string, payload)
}
```

This practice ensures API endpoints follow RESTful conventions, improves API discoverability, and allows for proper caching mechanisms.