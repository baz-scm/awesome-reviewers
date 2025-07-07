---
title: Use proper types
description: 'Maintain code clarity by using appropriate type declarations and parameter
  passing conventions:


  1. **Prefer explicit types over `auto` when the type is known and simple**:'
repository: tensorflow/tensorflow
label: Code Style
language: Other
comments_count: 10
repository_stars: 190625
---

Maintain code clarity by using appropriate type declarations and parameter passing conventions:

1. **Prefer explicit types over `auto` when the type is known and simple**:
```cpp
// Instead of:
auto device_ordinal = 0;

// Prefer:
int device_ordinal = 0;
```

2. **Use prefix form (`++i`) instead of postfix (`i++`) in loops** for better performance with non-primitive types:
```cpp
// Instead of:
for (int i = 0; i < perm.NumElements(); i++)

// Prefer:
for (int i = 0; i < perm.NumElements(); ++i)
```

3. **Mark variables as `const` when they're not modified**:
```cpp
// Instead of:
std::vector<TypeParam> input_data = CastVector<TypeParam>({1, 2, 3, 4, 5, 6});

// Prefer:
const std::vector<TypeParam> input_data = CastVector<TypeParam>({1, 2, 3, 4, 5, 6});
```

4. **Pass parameters appropriately**:
   - Pass lightweight objects like span by value: `void foo(absl::Span<int64_t> dims)` 
   - Pass `const&` for larger objects: `void foo(const std::vector<int>& vec)`
   - Mark function parameters as `const` when they're not modified

5. **Use C++-style casts instead of C-style casts**:
```cpp
// Instead of:
*itr = bfloat16(data[i]);
rescaled_6 = (int64_t)std::round(6.0f / input_qtype.getScale()) + input_qtype.getZeroPoint();

// Prefer:
*itr = static_cast<bfloat16>(data[i]);
rescaled_6 = static_cast<int64_t>(std::round(6.0f / input_qtype.getScale())) + input_qtype.getZeroPoint();
```

6. **Put variables ahead of values being compared to**:
```cpp
// Instead of:
if (0 > crop_window_vec(2) || 0 > crop_window_vec(3))

// Prefer:
if (crop_window_vec(2) < 0 || crop_window_vec(3) < 0)
```