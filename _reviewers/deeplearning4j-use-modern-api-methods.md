---
title: Use modern API methods
description: When implementing algorithms with numerical libraries like ND4J, always
  prefer the most direct and type-safe API methods over older patterns. This improves
  code clarity, prevents subtle bugs, and often leads to better performance.
repository: deeplearning4j/deeplearning4j
label: Algorithms
language: Markdown
comments_count: 4
repository_stars: 14036
---

When implementing algorithms with numerical libraries like ND4J, always prefer the most direct and type-safe API methods over older patterns. This improves code clarity, prevents subtle bugs, and often leads to better performance.

Key practices:
1. Use `createFromArray` instead of `create` for array initialization, as it has clear overloads for all primitive types:
```java
{% raw %}
// Preferred:
double arr_2d[][] = {{1.0,2.0,3.0},{4.0,5.0,6.0}};
INDArray x_2d = Nd4j.createFromArray(arr_2d);

// Avoid:
double[] flat = ArrayUtil.flattenDoubleArray(myDoubleArray);
int[] shape = {rows, cols};
INDArray myArr = Nd4j.create(flat, shape, 'c');
{% endraw %}
```

2. Prefer direct parameter methods over shape arrays for common operations:
```java
// Preferred:
INDArray x = Nd4j.zeros(DataType.DOUBLE, 5);

// Avoid:
int[] shape = {5};
INDArray x = Nd4j.zeros(shape, DataType.DOUBLE);
```

3. When handling arrays with different data types, explicitly use `castTo` for proper type conversion:
```java
// When types don't match
INDArray x = Nd4j.zeros(5, DataType.DOUBLE);
INDArray y = Nd4j.zeros(5, DataType.INT);

// Preferred:
INDArray result = x.add(y.castTo(DataType.DOUBLE));

// Avoid - will throw exception:
INDArray result = x.add(y);
```

Following these practices leads to more efficient algorithm implementations with fewer errors and better maintainability.