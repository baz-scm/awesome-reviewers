---
title: "Proper Use of Suspense in Next.js Components"
description: "When building Next.js applications that leverage server-side rendering (SSR) or Partial Prerendering (PPR), it is essential to wrap components that access dynamic or non-deterministic values in Suspense boundaries with appropriate fallbacks."
repository: "vercel/next.js"
label: "Next.js"
language: "JavaScript"
comments_count: 4
repository_stars: 133000
---

When building Next.js applications that leverage server-side rendering (SSR) or Partial Prerendering (PPR), it is essential to wrap components that access dynamic or non-deterministic values (e.g. random values, current time, request-specific data) in Suspense boundaries with appropriate fallbacks. This ensures proper handling of components that cannot be statically prerendered, preventing hydration mismatches and improving performance.

Specifically, developers should:

1. Identify components in their Next.js application that rely on dynamic or non-deterministic data.
2. Wrap these components in a Suspense boundary, providing a fallback UI to display while the dynamic content is being fetched.
3. Ensure that the fallback UI is visually consistent with the final rendered component, to maintain a seamless user experience.

Here is an example of the correct usage of Suspense in a Next.js component:

```jsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <section>
      <h1>This will be prerendered</h1>
      <Suspense fallback={<FallbackComponent />}>
        <DynamicComponent />
      </Suspense>
    </section>
  )
}
```

By following this pattern, developers can leverage the benefits of Next.js's SSR and PPR capabilities while ensuring a robust and consistent user experience, even for components that rely on dynamic data.