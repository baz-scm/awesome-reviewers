---
title: Cross-platform algorithm optimization
description: 'When implementing algorithms that need to execute efficiently across
  different platforms, consider both compile-time and runtime optimizations:


  1. For template-heavy code, use explicit instantiations to improve compilation speed
  and avoid compiler limitations on specific platforms:'
repository: deeplearning4j/deeplearning4j
label: Algorithms
language: Other
comments_count: 4
repository_stars: 14036
---

When implementing algorithms that need to execute efficiently across different platforms, consider both compile-time and runtime optimizations:

1. For template-heavy code, use explicit instantiations to improve compilation speed and avoid compiler limitations on specific platforms:
   ```cpp
   // Use CMake to generate explicit template instantiations 
   // in separate compilation units
   #cmakedefine LIBND4J_TYPE_GEN 
   
   #include <ops/declarable/helpers/cpu/summaryReductions.hpp>
   ```

2. Use platform-agnostic type definitions to ensure consistent behavior, particularly when interfacing between languages like C++ and Java:
   ```cpp
   // Prefer explicit sized types rather than platform-dependent types
   typedef int Nd4jInt;  // For 32-bit integers
   typedef long long Nd4jLong;  // For 64-bit integers
   ```

3. Avoid calling member functions from constructors when inlining might be deactivated:
   ```cpp
   // Instead of: 
   // if (rootSeed == 0)
   //     rootSeed = currentMilliseconds();
   
   // Directly use the implementation:
   if (rootSeed == 0){
       auto s = std::chrono::system_clock::now().time_since_epoch();
       rootSeed = std::chrono::duration_cast<std::chrono::milliseconds>(s).count();
   }
   ```

4. When working with hardware acceleration libraries like CUDA, create wrapper classes that handle version differences and provide consistent error handling:
   ```cpp
   template<typename Op, typename ...Args>
   FORCEINLINE void callCudnnIfNoErr(cudnnStatus_t &err, Op op, Args&&... args) {
       if(err==CUDNN_STATUS_SUCCESS) {
           err = op(std::forward<Args>(args)...);
           if(err) {
               nd4j_printf("Cudnn error code %s\n", cudnnGetErrorString(err));
           }
       }
   }
   ```

Always document platform-specific considerations directly in the code to help future developers understand your optimization decisions.