---
title: CMake custom command design
description: When implementing CMake build automation for code generation, carefully
  choose between `add_custom_command` and `add_custom_target` based on your execution
  requirements. Use `add_custom_command` with explicit OUTPUT and DEPENDS for files
  that should be automatically generated when missing or when dependencies change.
  Add `add_custom_target` only when you...
repository: tree-sitter/tree-sitter
label: CI/CD
language: Txt
comments_count: 2
repository_stars: 21799
---

When implementing CMake build automation for code generation, carefully choose between `add_custom_command` and `add_custom_target` based on your execution requirements. Use `add_custom_command` with explicit OUTPUT and DEPENDS for files that should be automatically generated when missing or when dependencies change. Add `add_custom_target` only when you need manual invocation capability in addition to automatic dependency resolution.

Always specify clear OUTPUT, DEPENDS, WORKING_DIRECTORY, and COMMENT parameters to make the build process transparent and debuggable. Test that your custom commands work both automatically (when dependencies change) and can be validated independently.

Example:
```cmake
# Automatic generation when src/parser.c is missing or grammar.json changes
add_custom_command(OUTPUT "${CMAKE_CURRENT_SOURCE_DIR}/src/parser.c"
                   DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/src/grammar.json"
                   COMMAND "${TREE_SITTER_CLI}" generate src/grammar.json
                            --abi=${TREE_SITTER_ABI_VERSION}
                   WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
                   COMMENT "Generating parser.c")

# Optional: Add target for manual invocation
add_custom_target(generate DEPENDS src/parser.c)
```

Document the purpose and usage of each custom target to avoid confusion about when automatic vs manual execution occurs.