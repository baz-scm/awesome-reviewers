---
title: Eliminate redundant null checks
description: Avoid unnecessary null checks when the called function already handles
  null cases, and use references instead of pointers when null values are guaranteed
  not to occur.
repository: llvm/llvm-project
label: Null Handling
language: C++
comments_count: 5
repository_stars: 33702
---

Avoid unnecessary null checks when the called function already handles null cases, and use references instead of pointers when null values are guaranteed not to occur.

Many codebases contain redundant null checks that add complexity without providing safety benefits. This occurs in several patterns:

1. **Double-checking optionals**: When extracting values from optionals, avoid checking both the optional's validity and the extracted value if the extraction method already handles empty cases.

2. **Redundant pre-checks**: Don't check for null before calling functions that already return null for invalid inputs.

3. **Use references for non-null guarantees**: When a parameter is guaranteed to be non-null by preconditions, use references instead of pointers to make this contract explicit.

**Examples:**

```cpp
// ❌ Redundant: AsCString() already returns nullptr for empty strings
auto mod_name = m_opaque_sp->GetObjectName();
if (!mod_name) {
    return nullptr;
}
return mod_name.AsCString();

// ✅ Simplified: Let AsCString() handle the empty case
auto mod_name = m_opaque_sp->GetObjectName();
return mod_name.AsCString();

// ❌ Redundant optional checking
std::optional<mlir::FlatSymbolRefAttr> aliasee = op.getAliaseeAttr();
if (aliasee && *aliasee)
    return matchAndRewriteAlias(op, *aliasee, ...);

// ✅ Simplified optional handling
if (std::optional<llvm::StringRef> aliasee = op.getAliasee())
    return matchAndRewriteAlias(op, *aliasee, ...);

// ❌ Using pointer when null is impossible
int processSymbol(const Symbol *symbol) {
    // symbol can't be NULL due to preconditions
}

// ✅ Use reference to express non-null contract
int processSymbol(const Symbol &symbol) {
    // Contract is clear: symbol cannot be null
}
```

Document null safety assumptions in comments when the non-null guarantee isn't obvious from the function signature, and add explicit null checks (like `LIBC_CRASH_ON_NULLPTR`) only where parameters should never be null but the type system cannot enforce this.