---
title: Optimize hardware acceleration
description: AI systems should use the most performant hardware acceleration libraries
  and carefully manage hardware-specific dependencies. Prefer Intel MKL over OpenBLAS
  for CPU operations as it provides superior performance for matrix calculations critical
  to neural networks and machine learning algorithms. Keep CPU and GPU dependencies
  cleanly separated to support...
repository: deeplearning4j/deeplearning4j
label: AI
language: Xml
comments_count: 2
repository_stars: 14036
---

AI systems should use the most performant hardware acceleration libraries and carefully manage hardware-specific dependencies. Prefer Intel MKL over OpenBLAS for CPU operations as it provides superior performance for matrix calculations critical to neural networks and machine learning algorithms. Keep CPU and GPU dependencies cleanly separated to support different deployment scenarios.

Example:
```xml
<!-- Preferred: Use full MKL instead of OpenBLAS or MKL-DNN -->
<dependency>
    <groupId>org.bytedeco</groupId>
    <artifactId>mkl</artifactId>
    <version>${mkl.javacpp.version}</version>
    <classifier>${dependency.platform}</classifier>
</dependency>

<!-- Avoid adding CPU-specific dependencies to modules that need GPU-only builds -->
<!-- Even test-scoped native dependencies can break CUDA-only CI builds -->
```

This approach ensures optimal performance for AI model training and inference while maintaining compatibility across different hardware configurations.