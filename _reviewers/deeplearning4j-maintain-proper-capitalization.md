---
title: Maintain proper capitalization
description: 'Always use correct and consistent capitalization for product names,
  class names, and method names throughout code and documentation. Pay special attention
  to:'
repository: deeplearning4j/deeplearning4j
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 14036
---

Always use correct and consistent capitalization for product names, class names, and method names throughout code and documentation. Pay special attention to:

1. Framework names: `SameDiff` (not `samediff` or `Samediff`)
2. External frameworks: `TensorFlow` (not `Tensorflow`) 
3. Method names: `SameDiff.importFrozenTF` (maintaining correct capitalization patterns)

Consistent capitalization improves readability, searchability, and aligns with official naming conventions. When documenting naming behaviors, also be precise about how names are generated when not explicitly provided.

Example:
```java
// Incorrect
SDVariable result = samediff.var("myVar", Nd4j.create(shape));
samediff.importFrozenTF(modelPath);

// Correct
SDVariable result = sameDiff.var("myVar", Nd4j.create(shape));
sameDiff.importFrozenTF(modelPath);
```

In documentation, maintain the same capitalization standards and be explicit about naming patterns, including when names are auto-generated based on operation names.