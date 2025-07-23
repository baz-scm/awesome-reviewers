---
title: Optimize React components
description: 'Apply these React optimization techniques to improve component performance
  and maintainability:


  1. **Use stable, unique keys for list items** - Avoid using array indices as keys
  when rendering lists that can change. Instead, use unique identifiers from your
  data.'
repository: RooCodeInc/Roo-Code
label: React
language: TSX
comments_count: 4
repository_stars: 17288
---

Apply these React optimization techniques to improve component performance and maintainability:

1. **Use stable, unique keys for list items** - Avoid using array indices as keys when rendering lists that can change. Instead, use unique identifiers from your data.

```jsx
{/* Avoid this */}
{patterns.map((item, index) => (
  <div key={`${item.pattern}-${index}`} className="ml-5 flex items-center gap-2">
    {/* content */}
  </div>
))}

{/* Prefer this */}
{patterns.map((item) => (
  <div key={item.pattern} className="ml-5 flex items-center gap-2">
    {/* content */}
  </div>
))}
```

2. **Memoize computed values and callbacks** - Use React.useMemo() for arrays/objects and useCallback() for functions to prevent unnecessary recreations during renders.

```jsx
// Avoid recreating arrays/objects on every render
const toolGroups = React.useMemo(() => [
  // array contents
], [/* dependencies */]);
```

3. **Use React refs instead of direct DOM manipulation** - Avoid document.querySelector and similar methods in favor of React's ref system.

```jsx
// Instead of:
const enhanceButton = document.querySelector('[aria-label*="enhance"]');

// Prefer:
const enhanceButtonRef = useRef(null);
// Then pass the ref to the component
<Button ref={enhanceButtonRef} aria-label="enhance" />
```

4. **Simplify state management** - Keep state minimal and focused on what's needed. Use simple values over complex collections when possible.

```jsx
// Instead of tracking all instances in a collection:
const [followUpAnswered, setFollowUpAnswered] = useState<Set<number>>(new Set());

// Consider tracking just what's needed:
const [currentFollowUpTs, setCurrentFollowUpTs] = useState<number | null>(null);
```