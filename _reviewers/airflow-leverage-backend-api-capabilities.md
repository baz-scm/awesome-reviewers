---
title: Leverage backend API capabilities
description: When consuming APIs in frontend applications, utilize the backend capabilities
  rather than reimplementing equivalent functionality in the frontend. This reduces
  code complexity, improves performance, and maintains a clean separation of concerns.
repository: apache/airflow
label: API
language: TSX
comments_count: 4
repository_stars: 40858
---

When consuming APIs in frontend applications, utilize the backend capabilities rather than reimplementing equivalent functionality in the frontend. This reduces code complexity, improves performance, and maintains a clean separation of concerns.

Key practices:
1. **Use pagination parameters**: Request only the data you need using the API's pagination features rather than fetching everything and filtering client-side.
```typescript
// AVOID
const { data } = useAssetServiceGetAssets();
const visibleItems = data?.assets.slice(0, MAX_VISIBLE);

// PREFER
const { data } = useAssetServiceGetAssets({
  limit: MAX_VISIBLE,
  offset: 0
});
```

2. **Request appropriate content formats**: Use Accept headers to get data in the format best suited for your needs.
```typescript
// When raw logs are needed
useTaskInstanceServiceGetLog({
  // Other parameters...
  accept: "text/plain" // Get raw logs directly
});
```

3. **Use server-side filtering**: Leverage backend filtering capabilities instead of making multiple requests and combining results client-side.
```typescript
// AVOID
const { data: dataByName } = useAssetServiceGetAssets({ namePattern: searchValue });
const { data: dataByGroup } = useAssetServiceGetAssets({ groupPattern: searchValue });
// Merging results in the frontend...

// PREFER - Extend the backend to support this use case
const { data } = useAssetServiceGetAssets({ search: searchValue }); // Searches across multiple fields
```

4. **Extend the backend when needed**: If you need functionality that isn't available in the API, consider extending the backend API rather than creating complex workarounds in the frontend.

Following these practices leads to more maintainable code, better performance, and a clearer separation of responsibilities between frontend and backend.