---
title: User-friendly documentation examples
description: Documentation should guide users toward best practices through clear
  examples. Begin with positive patterns before covering pitfalls, clarify all function
  parameters, and recommend appropriate methods for common tasks.
repository: deeplearning4j/deeplearning4j
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 14036
---

Documentation should guide users toward best practices through clear examples. Begin with positive patterns before covering pitfalls, clarify all function parameters, and recommend appropriate methods for common tasks.

When writing examples:
1. Use correct API naming conventions (e.g., 'INDArray' not 'IndArray')
2. Include parameter descriptions in comments for complex methods
3. Demonstrate the most appropriate methods for new users, avoiding potentially confusing APIs
4. Organize related functionality into logical sections
5. Indicate when showing only a subset of available functionality

```java
// GOOD: Begin with positive examples, show parameter details
INDArray x = Nd4j.linspace(1, 10, 5); // start, stop, count
// [1.0000, 3.2500, 5.5000, 7.7500, 10.0000]

// GOOD: Recommend beginner-friendly methods
float[] vector = x.toFloatVector(); // Better than .data().asDouble()

// GOOD: Group related functionality with proper naming
// Reduction/accumulation operations:
x.sum();  // Sum of all elements
x.min();  // Minimum value
x.max();  // Maximum value

// BETTER: Move "don't do this" examples to the end
// Common pitfalls to avoid:
// INDArray x3 = x.add(x2); // Error if datatypes don't match
```