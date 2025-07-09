---
title: Next.js async behavior
description: 'Understand and correctly implement the asynchronous behavior of Next.js
  APIs and components. Follow these guidelines:


  1. Add `<Suspense>` boundaries around components that use hooks that can trigger
  suspense, such as `useSearchParams` in the Next.js App Router:'
repository: elie222/inbox-zero
label: Next
language: TSX
comments_count: 3
repository_stars: 8267
---

Understand and correctly implement the asynchronous behavior of Next.js APIs and components. Follow these guidelines:

1. Add `<Suspense>` boundaries around components that use hooks that can trigger suspense, such as `useSearchParams` in the Next.js App Router:

```tsx
<Suspense>
  <ComponentUsingSearchParams />
</Suspense>
```

2. Don't await synchronous Next.js functions. For example, `cookies()` from 'next/headers' returns a synchronous object:

```tsx
// Incorrect
const cookieStore = await cookies();

// Correct
const cookieStore = cookies();
```

3. Next.js page props like `searchParams` are regular objects, not Promises - handle them correctly:

```tsx
// Incorrect
export default async function Page(props: {
  searchParams: Promise<{ param?: string }>;
}) {
  const searchParams = await props.searchParams;
  // ...
}

// Correct
export default async function Page({ 
  searchParams 
}: {
  searchParams: { param?: string };
}) {
  // ...
}
```

Correctly identifying when to use asynchronous patterns like `Suspense` and `await` improves application stability and performance.