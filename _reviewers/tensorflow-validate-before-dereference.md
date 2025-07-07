---
title: Validate before dereference
description: Always check that pointers, optional values, and results of type casts
  are valid before dereferencing or using them. This prevents null pointer exceptions,
  undefined behavior, and potential crashes in production.
repository: tensorflow/tensorflow
label: Null Handling
language: Other
comments_count: 5
repository_stars: 190625
---

Always check that pointers, optional values, and results of type casts are valid before dereferencing or using them. This prevents null pointer exceptions, undefined behavior, and potential crashes in production.

For pointers obtained from operations or external sources:
```cpp
// Before accessing a pointer's members
if (value.getDefiningOp() != nullptr) {
  // Now safe to use value.getDefiningOp()->getResult(0)
}
```

For optional values, verify presence before access:
```cpp
auto shared_library_dir = FindDispatchOption(options, num_options, kDispatchOptionSharedLibraryDir);
if (shared_library_dir.HasValue()) {
  shared_library_dir_opt.emplace(std::any_cast<const char*>(shared_library_dir.Value()));
}
```

For dynamic casts, check success before using the result:
```cpp
auto input_type = input_value.getType().dyn_cast<RankedTensorType>();
if (!input_type) {
  op->emitOpError("Input type not ranked tensor");
  return nullptr;
}
```

When designing APIs, preserve nullability expectations to maintain compatibility:
```cpp
// Check parameters that might be null rather than requiring non-null
if (run_metadata != nullptr) {
  // Only use run_metadata when it's provided
}
```