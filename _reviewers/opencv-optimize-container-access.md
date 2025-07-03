---
title: Optimize container access
description: Choose efficient container types and optimize access patterns in performance-critical
  code. Avoid operations that cause hidden allocations and minimize overhead when
  accessing container elements.
repository: opencv/opencv
label: Performance Optimization
language: Other
comments_count: 5
repository_stars: 82865
---

Choose efficient container types and optimize access patterns in performance-critical code. Avoid operations that cause hidden allocations and minimize overhead when accessing container elements.

**Key practices:**

1. **Avoid in-place operations** that cause hidden copies:
   ```cpp
   // Bad: causes hidden .clone() call
   inputMat.convertTo(inputMat, CV_8UC1, 1.0 / 256);
   
   // Good: use a separate destination
   inputMat.convertTo(convertedMat, CV_8UC1, 1.0 / 256);
   ```

2. **Use flat arrays instead of nested containers** for better cache locality and reduced overhead:
   ```cpp
   // Bad: vector of vectors has high overhead
   std::vector<std::vector<uint16_t>> hist256(channels, std::vector<uint16_t>(256, 0));
   
   // Good: single flat vector
   std::vector<uint16_t> hist256(channels * 256, 0);
   ```

3. **Extract raw pointers** from containers for tight loops:
   ```cpp
   // Bad: repeatedly accessing vector methods in tight loops
   for (int i = 0; i < size; i++) {
       result += hist256[c][i];
   }
   
   // Good: extract pointer once before loop
   std::vector<uint16_t> hist256vec(256, 0);
   uint16_t* hist256 = hist256vec.data();
   for (int i = 0; i < size; i++) {
       result += hist256[i];
   }
   ```

4. **Use stack allocation when possible** instead of dynamic allocation:
   ```cpp
   // Bad: unnecessary heap allocation
   if (condition) {
       std::vector<uchar> *dst = new std::vector<uchar>(size);
       // use dst
       delete dst;
   }
   
   // Good: stack allocation with proper scope
   std::vector<uchar> dst;
   if (condition) {
       dst.resize(size);
       // use dst
   }
   ```

Choose container types based on actual performance measurements rather than assumptions, as the best data structure can vary by platform and usage pattern.
