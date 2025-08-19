---
title: explicit null state management
description: Make null state checks explicit and comprehensive rather than using implicit
  return values or redundant fields. Use dedicated methods like `ContainsNull()` to
  clearly indicate null state, avoid duplicate null tracking when child objects already
  maintain null state, and ensure hierarchical null checks cover all levels (self
  and children).
repository: duckdb/duckdb
label: Null Handling
language: Other
comments_count: 6
repository_stars: 32061
---

Make null state checks explicit and comprehensive rather than using implicit return values or redundant fields. Use dedicated methods like `ContainsNull()` to clearly indicate null state, avoid duplicate null tracking when child objects already maintain null state, and ensure hierarchical null checks cover all levels (self and children).

For efficiency, only perform null-setting operations when actually needed:
```cpp
// Good: Explicit null check with efficient setting
A_TYPE input = A_TYPE::ConstructType(state, i);
if (input.ContainsNull()) {
    FlatVector::SetNull(result, i, true);
    continue;
}

// Good: Hierarchical null detection
bool ContainsNull() {
    return is_null || a_val.is_null || b_val.is_null;
}

// Bad: Redundant null fields when children track null state
struct StructTypeBinary {
    A_TYPE a_val;        // Already has is_null field
    B_TYPE b_val;        // Already has is_null field  
    bool a_is_null;      // Redundant!
    bool b_is_null;      // Redundant!
};
```

This pattern prevents null-related bugs by making null state explicit, reduces redundancy, and ensures comprehensive null detection across complex nested structures.