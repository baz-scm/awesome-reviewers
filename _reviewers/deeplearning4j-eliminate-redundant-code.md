---
title: Eliminate redundant code
description: 'Keep code clean by removing all forms of redundancy that affect readability
  and maintainability. This includes:


  1. Avoid duplicate macro/constant definitions that could cause conflicts or confusion'
repository: deeplearning4j/deeplearning4j
label: Code Style
language: Other
comments_count: 3
repository_stars: 14036
---

Keep code clean by removing all forms of redundancy that affect readability and maintainability. This includes:

1. Avoid duplicate macro/constant definitions that could cause conflicts or confusion
   ```c++
   // BAD - duplicated macro definition
   #define ARRAY_IS_VIEW 33554432
   #define ARRAY_IS_VIEW 33554432  // Duplicate!
   
   // GOOD - defined once
   #define ARRAY_IS_VIEW 33554432
   ```

2. Remove debug print statements from production code unless they're part of error handling
   ```c++
   // BAD - debug statement in production code
   registerUse({&res}, {this});
   sd_printf("After before exec\n",0);  // Debug print in production code
   
   // GOOD - only in error paths or removed entirely
   registerUse({&res}, {this});
   // No unnecessary print statements
   ```

3. Keep configuration files clean without redundant/duplicate content (such as repeated license headers)

Each form of redundancy impacts code readability and increases maintenance burden. When reviewing code, make sure information is stated once and only once where appropriate.