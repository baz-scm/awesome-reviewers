---
title: API documentation accuracy
description: Ensure API documentation accurately describes actual behavior and avoids
  subjective commentary that may become outdated. Documentation should clearly explain
  how features interact, what the expected behavior is, and avoid qualitative assessments
  about performance or quality that can change over time.
repository: helix-editor/helix
label: API
language: Markdown
comments_count: 2
repository_stars: 39026
---

Ensure API documentation accurately describes actual behavior and avoids subjective commentary that may become outdated. Documentation should clearly explain how features interact, what the expected behavior is, and avoid qualitative assessments about performance or quality that can change over time.

When documenting APIs or software integrations, focus on factual descriptions of functionality rather than opinions about how well something works. For example, instead of saying "Seems to work less well than Dance" in a comparison table, simply list the available options without subjective commentary.

Additionally, when API behavior might be misunderstood, provide clear explanations. For instance, if documentation suggests "only one language server can be used for each feature" but the actual behavior allows multiple servers for some features like diagnostics, clarify this discrepancy with additional documentation.

Example of good practice:
```toml
# Clear, factual description
[language-server.efm-lsp-prettier]
command = "efm-langserver"
# Explains actual behavior without opinion
config = { documentFormatting = true }
```

This approach keeps documentation maintainable, prevents user confusion, and ensures that API behavior is accurately represented to developers.