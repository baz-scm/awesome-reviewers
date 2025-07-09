---
title: Prevent object recreations
description: 'Avoid creating new objects and functions repeatedly during renders to
  reduce memory pressure and improve performance. Implement these practices:


  1. **Move static data outside components:**'
repository: shadcn-ui/ui
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 90568
---

Avoid creating new objects and functions repeatedly during renders to reduce memory pressure and improve performance. Implement these practices:

1. **Move static data outside components:**
   ```jsx
   // Instead of this:
   function MyComponent() {
     const spinnerBars = [
       { animationDelay: -1.2, rotate: 0 },
       { animationDelay: -1.1, rotate: 30 },
       // ...more items
     ];
     // component code
   }

   // Do this:
   const spinnerBars = Array.from({ length: 12 }, (_, index) => ({
     animationDelay: -1.2 + 0.1 * index,
     rotate: 30 * index
   }));

   function MyComponent() {
     // component code
   }
   ```

2. **Avoid inline function definitions in event handlers:**
   ```jsx
   // Instead of this:
   <Button onClick={() => scrollTo(index)} />

   // Do this:
   const handleScrollTo = (index) => () => scrollTo(index);
   <Button onClick={handleScrollTo(index)} />
   ```

3. **Prevent unnecessary object instantiation:**
   ```jsx
   // Instead of this:
   return new Date(date) >= new Date(now)

   // Do this when objects already exist:
   return date >= now
   ```

These optimizations reduce garbage collection overhead and improve rendering performance, especially in components that render frequently or in large lists.