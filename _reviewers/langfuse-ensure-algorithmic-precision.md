---
title: Ensure algorithmic precision
description: When implementing algorithms, ensure they perform exactly the operations
  needed without introducing unintended side effects or limitations. Verify all calculations
  produce correct results and avoid assumptions that restrict applicability.
repository: langfuse/langfuse
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 13574
---

When implementing algorithms, ensure they perform exactly the operations needed without introducing unintended side effects or limitations. Verify all calculations produce correct results and avoid assumptions that restrict applicability.

Three common mistakes to avoid:

1. Adding arbitrary constants or modifiers that distort results
   ```typescript
   // Incorrect: Arbitrary constant distorts the percentage
   const percentage = 300 + (usage / MAX_EVENTS_FREE_PLAN) * 100;
   
   // Correct: Calculate the actual percentage
   const percentage = (usage / MAX_EVENTS_FREE_PLAN) * 100;
   ```

2. Using overly broad operations that may affect unintended elements
   ```typescript
   // Incorrect: Removes ALL 'metrics' segments
   const segments = folder.filter(segment => segment !== 'metrics');
   
   // Correct: Only removes 'metrics' if it's the last segment
   const segments = folder[folder.length - 1] === 'metrics' ? folder.slice(0, -1) : folder;
   ```

3. Introducing unnecessary constraints that limit applicability
   ```typescript
   // Incorrect: Forces minimum of 1, unsuitable for fractional values
   const roundTo = Math.max(1, Math.pow(10, magnitude) / 5);
   
   // Correct: Allows appropriate scaling for all value ranges
   const roundTo = Math.pow(10, magnitude) / 5;
   ```

Ensure your algorithms precisely target the intended elements and handle all possible input values correctly.