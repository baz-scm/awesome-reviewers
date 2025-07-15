---
title: Endpoints for evolving data
description: Design dedicated API endpoints for data that changes frequently or grows
  over time, rather than hardcoding such information in frontend files. This pattern
  ensures that applications remain maintainable as backend data evolves.
repository: prowler-cloud/prowler
label: API
language: TypeScript
comments_count: 2
repository_stars: 11834
---

Design dedicated API endpoints for data that changes frequently or grows over time, rather than hardcoding such information in frontend files. This pattern ensures that applications remain maintainable as backend data evolves.

**When to apply:**
- When handling data collections that grow over time (e.g., compliance frameworks, check definitions)
- When data structures need to be accessible across multiple front-end components
- When information may need to be filtered or queried dynamically

**Example:**
Instead of:
```typescript
// ui/lib/lighthouse/helpers/complianceframeworks.ts
export const complianceFrameworks = {
  aws: [
    { id: "cis-aws", name: "CIS AWS Benchmark" },
    { id: "aws-foundational", name: "AWS Foundational Security Best Practices" },
    // Adding new frameworks requires code changes and deployment
  ]
};
```

Implement an API endpoint:
```typescript
// API service
app.get('/api/compliance-frameworks/:provider', (req, res) => {
  const provider = req.params.provider;
  return res.json(getComplianceFrameworksByProvider(provider));
});

// Frontend usage
const fetchFrameworks = async (provider) => {
  const response = await fetch(`/api/compliance-frameworks/${provider}`);
  return await response.json();
};
```

This approach eliminates maintenance overhead when adding new frameworks and allows for dynamic filtering and presentation options.