---
title: "Prefer Existence Checks in Next.js Components"
description: "When working with props, state, or other values in Next.js components that may be null, undefined, or contain error states, use existence checks rather than direct property access or value comparisons."
repository: "vercel/next.js"
label: "Next.js"
language: "JavaScript"
comments_count: 3
repository_stars: 133000
---

When working with props, state, or other values in Next.js components that may be null, undefined, or contain error states, use existence checks rather than direct property access or value comparisons. This helps prevent runtime exceptions and improves the reliability of your Next.js application.

For conditional rendering or operations in Next.js components:
```jsx
// ❌ Problematic - assumes 'previous' prop is a number
{previous > 0 ? <button onClick={previous}>Previous</button> : null}

// ✅ Better - checks if 'previous' prop exists at all
{previous ? <button onClick={previous}>Previous</button> : null}
```

When working with optional or error-prone properties in Next.js components:
```jsx
// ✅ Check for property existence before proceeding
export default function RemoteMdxPage({ mdxSource }) {
  if ("error" in mdxSource) {
    // Handle error state
    return <ErrorComponent error={mdxSource.error} />;
  }
  return <MDXClient {...mdxSource} />;
}
```

This approach applies to any value that could be null, undefined, or contain an error state in your Next.js components. Using the appropriate existence check pattern improves code safety, reliability, and readability.