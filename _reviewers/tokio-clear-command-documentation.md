---
title: Clear command documentation
description: When documenting shell commands in technical documentation, use the `shell`
  language identifier instead of `bash` as commands are typically relevant to any
  shell. Separate commands and their output into different code blocks to make it
  clearer what users should actually input. This improves readability and prevents
  users from accidentally copying output...
repository: tokio-rs/tokio
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 28989
---

When documenting shell commands in technical documentation, use the `shell` language identifier instead of `bash` as commands are typically relevant to any shell. Separate commands and their output into different code blocks to make it clearer what users should actually input. This improves readability and prevents users from accidentally copying output text as if it were commands.

For example, instead of:

```bash
$ cd tokio
$ cargo fuzz list
fuzz_linked_list
```

Use:

```shell
cd tokio
cargo fuzz list
```

```text
fuzz_linked_list
```

When documenting tool installation commands, include the `--locked` flag to protect users from dependency issues:

```shell
cargo install --locked cargo-docs-rs
```

This ensures developers can reproduce the exact same environment for development tools.