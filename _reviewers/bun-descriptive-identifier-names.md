---
title: Descriptive identifier names
description: Choose clear, consistent, and accurate identifiers that precisely reflect
  behavior and follow established patterns. This applies to function names, method
  names, variable types, and enum values.
repository: oven-sh/bun
label: Naming Conventions
language: C++
comments_count: 5
repository_stars: 79093
---

Choose clear, consistent, and accurate identifiers that precisely reflect behavior and follow established patterns. This applies to function names, method names, variable types, and enum values.

For functions and methods:
- Ensure implementation names match their API registration (e.g., use `"fail"` in `IDLOperation::call` to match the prototype table registration)
- Choose names that reflect complete behavior including edge cases (e.g., use `getIndex` instead of `getDirectIndex` when properties might be getters)
- Consider creating more descriptive methods like `isInt32AsAnyInt` instead of `isUInt32()` when the method handles multiple input formats

For types and constants:
- Prefer standardized type names (e.g., `int64_t` over `long long`) for better portability
- Align enum values with established API conventions (e.g., using `utf16` to match Node.js's `napi_get_value_string_utf16`)

Consistent and precise naming reduces bugs from misinterpreting an identifier's purpose, improves code readability, and makes integration with other libraries more intuitive.