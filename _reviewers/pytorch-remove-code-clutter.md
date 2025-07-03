---
title: Remove code clutter
description: 'Eliminate unnecessary code elements that add cognitive load without
  providing value. This includes:


  1. **Unused parameters** - Remove or mark parameters that are no longer used:'
repository: pytorch/pytorch
label: Code Style
language: Other
comments_count: 8
repository_stars: 91169
---

Eliminate unnecessary code elements that add cognitive load without providing value. This includes:

1. **Unused parameters** - Remove or mark parameters that are no longer used:
   ```cpp
   // Bad
   void blockReduceGammaBetaBackwardsHelper(..., bool check_x, bool check_y) {
     // check_y is never used
   }
   
   // Good
   void blockReduceGammaBetaBackwardsHelper(..., bool check_x) {
     // Removed unused parameter
   }
   
   // Alternative using C++17 features
   void blockReduceGammaBetaBackwardsHelper(..., bool check_x, [[maybe_unused]] bool check_y) {
     // Explicitly marking parameter as unused
   }
   ```

2. **Redundant prefixes** - Skip `this->` when class members don't shadow local variables:
   ```cpp
   // Bad
   this->dims_before = new_dims_before;
   this->dims_after = new_dims_after;
   
   // Good
   dims_before = new_dims_before;
   dims_after = new_dims_after;
   ```

3. **Typos in comments** - Fix comment typos to maintain code clarity:
   ```cpp
   // Bad
   /*transpoced*/ false
   
   // Good
   /*transposed*/ false
   ```

4. **Modern alternatives to C-arrays** - Prefer standard containers:
   ```cpp
   // Bad
   auto lhs_qa8dx_buffer = std::make_unique<int8_t[]>(
       m * (k + sizeof(float) + sizeof(int32_t))); // Allocate for LHS
   int8_t* lhs_qa8dx = lhs_qa8dx_buffer.get();
   
   // Good
   std::vector<int8_t> lhs_qa8dx_buffer(m * (k + sizeof(float) + sizeof(int32_t)));
   int8_t* lhs_qa8dx = lhs_qa8dx_buffer.data();
   ```

5. **Undefined local macros** - Clean up macros that are only needed temporarily:
   ```cpp
   // Bad
   #define C10_ALLOCATOR_CONFIG_PARSE_ENV(env, deprecated) ...
   // macro used
   // but never undefined
   
   // Good
   #define C10_ALLOCATOR_CONFIG_PARSE_ENV(env, deprecated) ...
   // macro used
   #undef C10_ALLOCATOR_CONFIG_PARSE_ENV
   ```

6. **Unnecessary forwards** - Remove unnecessary std::forward calls:
   ```cpp
   // Bad
   check_type(schema_arg, std::forward<IValueList>(args)[i_arg - 1]);
   
   // Good
   check_type(schema_arg, args[i_arg - 1]);
   ```

Removing clutter improves readability, reduces maintenance burden, and helps avoid subtle bugs.
