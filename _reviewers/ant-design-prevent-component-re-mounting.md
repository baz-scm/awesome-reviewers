---
title: Prevent component re-mounting
description: Maintain stable component structure to prevent unnecessary re-mounting
  and unmounting of child components. Conditional rendering that changes component
  tree structure can cause child components to lose state and trigger mount/unmount
  cycles, breaking components with mount effects.
repository: ant-design/ant-design
label: React
language: TSX
comments_count: 7
repository_stars: 95882
---

Maintain stable component structure to prevent unnecessary re-mounting and unmounting of child components. Conditional rendering that changes component tree structure can cause child components to lose state and trigger mount/unmount cycles, breaking components with mount effects.

Use techniques like refs to track rendering state, stable Context providers, and consistent component tree structure. Avoid patterns that conditionally return different component types or structures based on state changes.

Example of problematic pattern:
```tsx
const LazyComponent = ({ children, ...props }) => {
  const [lazy, setLazy] = React.useState(true);
  if (lazy) {
    return (
      <div onMouseEnter={() => setLazy(false)}>
        {children}
      </div>
    );
  }
  return <InternalTooltip {...props}>{children}</InternalTooltip>;
};
```

Better approach using refs to maintain structure:
```tsx
const needWrapMotionProviderRef = React.useRef(false);
needWrapMotionProviderRef.current = needWrapMotionProviderRef.current || motion === false;

if (needWrapMotionProviderRef.current) {
  return <MotionProvider motion={motion}>{children}</MotionProvider>;
}
```

This ensures components don't re-mount when conditions change, preserving component state and avoiding performance issues.