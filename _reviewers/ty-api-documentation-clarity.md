---
title: API documentation clarity
description: Ensure API documentation, including changelogs and feature descriptions,
  prioritizes user understanding over implementation details. Write descriptions that
  explain what users can expect from the API behavior rather than how it's technically
  implemented. Avoid redundant information when context is already established (e.g.,
  don't repeat "language server...
repository: astral-sh/ty
label: API
language: Markdown
comments_count: 4
repository_stars: 11919
---

Ensure API documentation, including changelogs and feature descriptions, prioritizes user understanding over implementation details. Write descriptions that explain what users can expect from the API behavior rather than how it's technically implemented. Avoid redundant information when context is already established (e.g., don't repeat "language server feature" under a "Server" section). Provide proper references and links to specifications or external documentation when mentioning technical concepts.

Example improvements:
- Instead of: "Implement non-stdlib stub mapping for classes and functions"
- Write: "Prefer the runtime definition, not the stub definition, on a go-to-definition request for a class or function"

- Instead of: "Add semantic token support for more identifiers"  
- Write: "Add [semantic token](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_semanticTokens) support for more identifiers"

This approach makes API documentation more accessible to users who need to understand functionality and behavior, not internal implementation choices.