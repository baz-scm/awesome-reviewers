---
title: Numerical stability practices
description: 'When implementing machine learning algorithms, ensure numerical correctness
  and stability by following these practices:


  1. Use appropriate default parameters based on research paper recommendations. For
  example, in AdaBelief, use smaller epsilon values as recommended by the authors:'
repository: deeplearning4j/deeplearning4j
label: AI
language: Java
comments_count: 5
repository_stars: 14036
---

When implementing machine learning algorithms, ensure numerical correctness and stability by following these practices:

1. Use appropriate default parameters based on research paper recommendations. For example, in AdaBelief, use smaller epsilon values as recommended by the authors:
```java
// Instead of this
public static final double DEFAULT_EPSILON = 1e-8;
// Use this
public static final double DEFAULT_EPSILON = 1e-14; // Follows paper recommendation
```

2. Add validation for parameter ranges, especially probability values:
```java
// Add checks like this for masking probabilities
Preconditions.checkArgument(maskProb > 0 && maskProb < 1, 
    "Probability must be between 0 and 1, got %s", maskProb);
Preconditions.checkArgument(maskTokenProb + randomTokenProb <= 1.0,
    "Sum of probabilities must be <= 1, got %s", maskTokenProb + randomTokenProb);
```

3. Include small epsilon values in calculations that could produce numerical instability:
```java
// When performing normalization or similar operations
SDVariable scale = SD.math.sqrt(squaredNorm.plus(1e-5)); // Prevents underflow
```

4. Use proper variable references rather than hardcoded names to ensure calculations are handled correctly:
```java
// Instead of this
return sd.math.abs(labels.sub(sd.getVariable("out"))).mean(1);
// Use this
return sd.math.abs(labels.sub(layerInput)).mean(1);
```

These practices help prevent subtle numerical bugs that can affect model convergence, training stability, and inference quality. They're especially important in deep learning where calculations involve many operations that could compound numerical errors.