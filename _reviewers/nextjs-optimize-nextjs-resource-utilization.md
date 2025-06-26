---
title: "Optimize Next.js Resource Utilization"
description: "As a code reviewer, I recommend the following practices to optimize resource utilization when implementing Next.js applications."
repository: "vercel/next.js"
label: "Next.js"
language: "JavaScript"
comments_count: 5
repository_stars: 133000
---

As a code reviewer, I recommend the following practices to optimize resource utilization when implementing Next.js applications:

1. **Leverage Server Components for Direct Data Fetching**: Fetch data directly from the database or other sources in Server Components, rather than routing through API endpoints. This eliminates unnecessary HTTP roundtrips and improves performance.

Example:
```javascript
// DON'T: Fetch through API Route
export default async function Component() {
  const data = await fetch('/api/data'); // Creates unnecessary HTTP roundtrip
  return <div>{data}</div>;
}

// DO: Fetch directly in Server Component
export default async function Component() {
  const data = await db.query('SELECT * FROM data'); // Direct database access
  return <div>{data}</div>;
}
```

2. **Optimize Module Preloading**: For memory-intensive applications, consider controlling module preloading by setting `preloadEntriesOnStart` to `false` in your `next.config.js`. This will load modules on-demand instead of at startup, helping to balance the initial memory footprint with runtime performance.

```javascript
// next.config.js
module.exports = {
  preloadEntriesOnStart: false, // Load modules on-demand instead of at startup
};
```

3. **Manage Memory-Intensive Operations**: Carefully monitor and optimize memory-intensive operations in your Next.js application to ensure efficient resource utilization across the entire system.

By following these practices, you can improve the performance and scalability of your Next.js applications while maintaining a low memory footprint.