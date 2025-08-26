---
title: Use meaningful identifiers
description: Choose identifiers that accurately represent their purpose, semantics,
  and relationship to the codebase. Names should be self-documenting and consistent
  with established patterns in the module or API.
repository: tree-sitter/tree-sitter
label: Naming Conventions
language: C
comments_count: 5
repository_stars: 21799
---

Choose identifiers that accurately represent their purpose, semantics, and relationship to the codebase. Names should be self-documenting and consistent with established patterns in the module or API.

Key principles:
- Avoid redefining language keywords with preprocessor macros (use descriptive alternatives like `force_inline` instead of redefining `inline`)
- Parameter names should reflect ownership semantics (`borrowed_item` vs `owned_item`)
- Type names should accurately describe their purpose (avoid misleading suffixes like `Entry` for non-collection elements)
- Maintain consistent naming patterns within APIs (use established prefixes like `ts_language_` consistently)
- Use self-explanatory representations (hexadecimal `0x25A1` instead of decimal `9633` for Unicode values)

Example of good naming:
```c
// Good: Clear ownership semantics
static inline void analysis_state_set__push_by_clone(
  AnalysisStateSet *self,
  AnalysisState *borrowed_item  // Clearly indicates caller retains ownership
) {
  // ...
}

// Good: Consistent API prefix and self-documenting hex value
int ts_language_symbol_type_is_named(const TSLanguage *self, TSSymbol typeId) {
  // Use 0x25A1 instead of 9633 for Unicode box character □
  while (iswspace(lexer->lookahead) || 0x25A1 == lexer->lookahead) {
    // ...
  }
}
```