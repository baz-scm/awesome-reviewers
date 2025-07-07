---
title: Separate test data
description: Large test data should be separated from test logic to improve readability
  and maintainability. Move test data into separate files or define as constants at
  the top of test files. This makes the test bodies clearer and easier to understand.
repository: tensorflow/tensorflow
label: Testing
language: Other
comments_count: 3
repository_stars: 190625
---

Large test data should be separated from test logic to improve readability and maintainability. Move test data into separate files or define as constants at the top of test files. This makes the test bodies clearer and easier to understand.

For example, instead of:
```cpp
TYPED_TEST(NonQuantizedIntDotGeneralTest, IntTestTypesTensorsWork2) {
  using StorageT = typename TypeParam::StorageT;
  const Shape shape_lhs({7, 3, 4});
  const Shape shape_rhs({7, 4});
  // ...

  Vector<int64_t> lhs_data_int{
      0,  1,  4,  1,  -2, -3, 0, 0, 6,  -1, 0,  0,  1,  0,  -2, 0,  1,
      3,  4,  -6, 2,  4,  4,  0, 0, -2, -1, 1,  -2, -3, 0,  2,  -3, 0,
      0,  -2, 4,  -7, 2,  2,  0, 4, 2,  0,  -6, 1,  1,  2,  -2, -2, 0,
      -1, -4, -1, 0,  -1, 1,  3, 1, 1,  -4, 0,  0,  1,  -1, 0,  4,  -2,
      0,  5,  0,  -1, 0,  2,  1, 2, -1, 1,  -3, -2, -6, -3, -1, -3};
  // ... test logic
}
```

Use:
```cpp
// At file scope or in a separate header
constexpr int64_t kLhsDataInt[] = {
  0,  1,  4,  1,  -2, -3, 0, 0, 6,  -1, 0,  0,  1,  0,  -2, 0,  1,
  3,  4,  -6, 2,  4,  4,  0, 0, -2, -1, 1,  -2, -3, 0,  2,  -3, 0,
  0,  -2, 4,  -7, 2,  2,  0, 4, 2,  0,  -6, 1,  1,  2,  -2, -2, 0,
  -1, -4, -1, 0,  -1, 1,  3, 1, 1,  -4, 0,  0,  1,  -1, 0,  4,  -2,
  0,  5,  0,  -1, 0,  2,  1, 2, -1, 1,  -3, -2, -6, -3, -1, -3
};

TYPED_TEST(NonQuantizedIntDotGeneralTest, IntTestTypesTensorsWork2) {
  using StorageT = typename TypeParam::StorageT;
  const Shape shape_lhs({7, 3, 4});
  const Shape shape_rhs({7, 4});
  // ...
  
  Vector<int64_t> lhs_data_int(std::begin(kLhsDataInt), std::end(kLhsDataInt));
  // ... test logic
}
```

Additionally, create separate, focused test cases for different data types or edge cases rather than handling them all in one test with conditional logic. This makes tests easier to maintain and provides clearer failure diagnostics.