---
title: consistent formatting preferences
description: 'Maintain consistent formatting and use concise, standard syntax throughout
  the codebase. This includes several specific formatting rules:


  1. **Preprocessor directives**: Do not add spaces after the `#` symbol'
repository: tree-sitter/tree-sitter
label: Code Style
language: Other
comments_count: 5
repository_stars: 21799
---

Maintain consistent formatting and use concise, standard syntax throughout the codebase. This includes several specific formatting rules:

1. **Preprocessor directives**: Do not add spaces after the `#` symbol
2. **Indentation**: Use consistent indentation sizes (e.g., 2 spaces for C/C++ files)  
3. **Shell variables**: Avoid wrapping variables in double quotes when it breaks parameter expansion
4. **String operations**: Use concise operators and built-in language features over verbose alternatives
5. **Conditional operators**: Prefer concise test operators (e.g., `-n` instead of `! -z`)

Examples:
```c
// Good - no space after #
#pragma warning(push)
#pragma GCC diagnostic push

// Bad - space after #
# pragma warning(push)
# pragma GCC diagnostic push
```

```cpp
// Good - concise string concatenation
auto path = binary_directory + "/" + filename;

// Bad - verbose string construction  
auto path = binary_directory + std::string("/") + std::string(filename);
```

```bash
# Good - concise test operator
if [[ -n "$variable" ]]; then

# Bad - verbose test combination
if [[ ! -z "$variable" ]]; then
```

These formatting preferences improve code readability and maintain consistency across different languages and contexts in the codebase.