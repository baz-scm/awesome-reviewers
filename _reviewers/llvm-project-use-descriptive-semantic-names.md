---
title: Use descriptive semantic names
description: Choose specific, meaningful names that clearly convey purpose and follow
  established codebase patterns. Avoid generic terms that could apply to many different
  concepts.
repository: llvm/llvm-project
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 33702
---

Choose specific, meaningful names that clearly convey purpose and follow established codebase patterns. Avoid generic terms that could apply to many different concepts.

**Key principles:**
- **Avoid overloaded generic terms**: Instead of generic names like `kind()` that "mean sooooo many different things," use specific descriptive names like `templateKind()` or `nameKind()` that clearly indicate what type of classification is being provided.

- **Follow capitalization conventions**: Variable names should start with capital letters where required by the codebase style. For example, `vAddr` should be `VirtualAddr` for better readability and consistency.

- **Use positive boolean naming**: Prefer positive constructions like `EnableMISchedLoadClustering` over negative ones like `DisableMISchedLoadClustering`. This creates clearer auto-generated method names like `enableXXX()` rather than confusing double negatives.

- **Follow established patterns**: Synthetic variants should use lowercase suffixes, attribute spellings should match existing conventions, and naming should be consistent with similar constructs in the codebase.

- **Prefer explicit over implicit**: Use fully qualified names rather than `using` declarations when it improves clarity, especially for types that might be ambiguous in context.

**Example:**
```cpp
// Avoid generic, overloaded terms
TemplateNameKind kind() const;  // ❌ Generic "kind"

// Use specific, descriptive names  
TemplateNameKind templateKind() const;  // ✅ Clear purpose

// Follow positive naming for booleans
def TuneDisableMISchedLoadClustering;  // ❌ Negative construction
def TuneEnableMISchedLoadClustering;   // ✅ Positive, clear methods
```