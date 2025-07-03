---
title: Simplify for readability
description: 'Complex expressions, especially nested ternary operations, reduce code
  readability and maintainability. Prefer simpler alternatives:


  1. Break down nested ternary operations into clear if-else statements:'
repository: apache/mxnet
label: Code Style
language: Other
comments_count: 7
repository_stars: 20801
---

Complex expressions, especially nested ternary operations, reduce code readability and maintainability. Prefer simpler alternatives:

1. Break down nested ternary operations into clear if-else statements:
```cpp
// Hard to read:
TBlob temp_mid_tblob = ((common::is_int(inputs[0].type_flag_) || inputs[0].type_flag_ == kBool) && !param.exp_is_int) ? 
    outputs[0] : inputs[0].type_flag_ == kBool ? 
    TBlob(...) : inputs[0];

// More readable:
if ((common::is_int(inputs[0].type_flag_) || inputs[0].type_flag_ == kBool) && !param.exp_is_int) {
    temp_mid_tblob = outputs[0];
} else if (inputs[0].type_flag_ == kBool) {
    temp_mid_tblob = TBlob(...);
} else {
    temp_mid_tblob = inputs[0];
}
```

2. Simplify boolean conditions and remove unnecessary parentheses:
```cpp
// Instead of:
const bool same_shape = (inputs[0].shape() == inputs[1].shape());

// Use:
const bool same_shape = inputs[0].shape() == inputs[1].shape();
```

3. Store frequently referenced values in well-named variables:
```cpp
// Extract shapes used multiple times
const auto& lhs_shape = inputs[0].shape();
const auto& rhs_shape = inputs[1].shape();
const bool same_shape = lhs_shape == rhs_shape;
```

4. Define constants for magic numbers instead of using literals:
```cpp
// Instead of:
const auto softrelu = (val > 20) ? val : ::log(1 + ::exp(val));

// Define a constant:
const float SOFTRELU_THRESHOLD = 20.0f;
const auto softrelu = (val > SOFTRELU_THRESHOLD) ? val : ::log(1 + ::exp(val));
```

5. Use const for loop iterators and function parameters when they're not modified:
```cpp
// Prefer:
for (const auto& kv : n.outputs) {
    // code
}
```

These practices improve code clarity, reduce cognitive load when reading the code, and make future maintenance easier.
