---
title: Extract complex conditions
description: When encountering complex conditional expressions or generic variable
  references, extract them into clearly named variables or use explicit identifiers
  to improve code readability and maintainability.
repository: facebook/yoga
label: Code Style
language: C
comments_count: 2
repository_stars: 18255
---

When encountering complex conditional expressions or generic variable references, extract them into clearly named variables or use explicit identifiers to improve code readability and maintainability.

For complex conditions, break them down into descriptive boolean variables:
```c
// Instead of:
childCrossMeasureMode = YGFloatIsUndefined(childCrossSize) || 
    (currentRelativeChild->resolvedDimensions[dim[crossAxis]]->unit == YGUnitAuto) 
    ? YGMeasureModeUndefined : YGMeasureModeExactly;

// Extract to:
bool hasUndefinedSize = YGFloatIsUndefined(childCrossSize);
bool hasAutoUnit = currentRelativeChild->resolvedDimensions[dim[crossAxis]]->unit == YGUnitAuto;
childCrossMeasureMode = (hasUndefinedSize || hasAutoUnit) 
    ? YGMeasureModeUndefined : YGMeasureModeExactly;
```

For generic references, prefer explicit, context-specific identifiers:
```c
// Instead of:
return node->layout.measuredDimensions[dim[crossAxis]];

// Use explicit:
return node->layout.measuredDimensions[YGDimensionHeight];
```

This practice makes code self-documenting, easier to debug, and reduces cognitive load when reading complex logic.