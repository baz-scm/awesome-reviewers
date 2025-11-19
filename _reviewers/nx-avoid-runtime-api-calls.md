---
title: Avoid runtime API calls
description: Components should not make external API calls for data that can be pre-generated
  at build time. Instead of fetching dynamic data during component rendering, inject
  pre-computed values as props to improve performance and reduce external dependencies.
repository: nrwl/nx
label: API
language: TSX
comments_count: 2
repository_stars: 27518
---

Components should not make external API calls for data that can be pre-generated at build time. Instead of fetching dynamic data during component rendering, inject pre-computed values as props to improve performance and reduce external dependencies.

When you have data that changes infrequently (like GitHub star counts, version numbers, or configuration data), fetch it during the build process and pass it into components rather than making runtime API calls.

Example of what to avoid:
```tsx
// ❌ Don't do this - runtime API call in component
useEffect(() => {
  const getStarCount = async () => {
    const response = await fetch('https://api.github.com/repos/nrwl/nx');
    const data = await response.json();
    setStarCount(data.stargazers_count);
  };
  getStarCount();
}, []);
```

Example of preferred approach:
```tsx
// ✅ Do this - pass pre-generated data as props
interface HeaderProps {
  starCount: number; // Fetched at build time
}

export function Header({ starCount }: HeaderProps) {
  return <span>{formatStarCount(starCount)}</span>;
}
```

This approach reduces client-side API calls, improves initial page load performance, and makes components more predictable and testable.