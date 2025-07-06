---
title: Ensure test determinism
description: 'Create reliable and reproducible tests by explicitly controlling test
  inputs and verifying function behavior doesn''t have unintended side effects. Two
  key practices to follow:'
repository: deeplearning4j/deeplearning4j
label: Testing
language: Java
comments_count: 2
repository_stars: 14036
---

Create reliable and reproducible tests by explicitly controlling test inputs and verifying function behavior doesn't have unintended side effects. Two key practices to follow:

1. When testing functions that shouldn't modify input parameters, verify the inputs remain unchanged:
```java
// Before function call
INDArray duplicateInput = inputMatrix.dup();

// Call function under test
PCA.pca_factor(inputMatrix, ...);

// Verify input wasn't modified
assertEquals(duplicateInput, inputMatrix);
```

2. Make tests deterministic by setting explicit seeds for any operations involving randomness:
```java
// Use a specific seed to ensure deterministic behavior
MultiLayerConfiguration conf = new NeuralNetConfiguration.Builder()
    .seed(2021) // Important: ensures consistent initialization for tests
    .dataType(DataType.DOUBLE)
    // other configuration
    .build();
```

Including these practices in your tests will help prevent flaky tests, make debugging easier, and ensure that test failures represent actual issues rather than side effects or randomness.