---
title: Code block formatting standards
description: 'When documenting code examples and shell commands in project documentation,
  follow these formatting standards to ensure consistency and clarity:


  1. **Use appropriate language specifiers**:'
repository: tokio-rs/tokio
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 28981
---

When documenting code examples and shell commands in project documentation, follow these formatting standards to ensure consistency and clarity:

1. **Use appropriate language specifiers**:
   - Use `shell` rather than `bash` for shell commands that work in any shell environment
   - ```shell
     cargo install --locked cargo-docs-rs
     ```

2. **Separate commands from their output**:
   - Place commands and their outputs in separate code blocks
   - Label output blocks with `text` to distinguish them from executable commands
   - ```shell
     cd tokio
     cargo fuzz list
     ```
     
     ```text
     fuzz_linked_list
     ```

3. **Include safety flags in installation commands**:
   - Always use `--locked` with installation commands to prevent dependency issues
   - ```shell
     cargo install --locked cargo-spellcheck
     ```

4. **Format spellcheck exceptions properly**:
   - Enclose code-related terms in backticks when they're flagged by spellcheck
   - Add non-code terms to the dictionary file (spellcheck.dic)
   - Remember to update the word count in the dictionary file header

These practices improve documentation readability and help users distinguish between what they should type and what they should expect to see as output.