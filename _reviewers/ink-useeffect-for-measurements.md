---
title: useEffect for measurements
description: When using functions that depend on rendered layout or DOM measurements,
  call them within useEffect hooks to ensure they execute after the component has
  rendered and layout calculations are complete.
repository: vadimdemedes/ink
label: React
language: Markdown
comments_count: 2
repository_stars: 31825
---

When using functions that depend on rendered layout or DOM measurements, call them within useEffect hooks to ensure they execute after the component has rendered and layout calculations are complete.

Functions like `measureElement()` return incorrect results (typically zero values) when called during the initial render phase, before the browser has calculated the actual layout. This timing issue can lead to incorrect component behavior or layout calculations.

```jsx
import { useEffect, useRef, useState } from 'react';

const MyComponent = () => {
  const boxRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    // Call measurement functions after render
    const { width, height } = measureElement(boxRef);
    setDimensions({ width, height });
  }, []);

  return <Box ref={boxRef}>Content</Box>;
};
```

This pattern ensures accurate measurements and prevents layout-dependent operations from executing prematurely, leading to more reliable component behavior.