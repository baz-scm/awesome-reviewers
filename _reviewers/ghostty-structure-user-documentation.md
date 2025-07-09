---
title: Structure user documentation
description: 'When documenting complex features or configuration options, structure
  your documentation with these four key elements:


  1. **Concise summary**: Begin with a brief, terse explanation of what the feature
  does'
repository: ghostty-org/ghostty
label: Documentation
language: Other
comments_count: 4
repository_stars: 32864
---

When documenting complex features or configuration options, structure your documentation with these four key elements:

1. **Concise summary**: Begin with a brief, terse explanation of what the feature does
2. **Problem statement**: Explain what specific user problem this feature solves, focusing on visible consequences to the end user
3. **Technical explanation**: Provide implementation details with appropriate depth
4. **Usage guidance**: Advise when and how users should apply this feature

For example, instead of:

```zig
/// When enabled (any value other than `off`), Ghostty replaces the `ssh` command
/// with a shell function to provide enhanced terminal compatibility and feature
/// propagation when connecting to remote hosts.
```

Prefer this structure:

```zig
///   * `term-only`
///
///     Automatically set the `TERM` environment variable to `xterm-256color` when
///     connecting to remote hosts using SSH.
///
///     By default, Ghostty identifies itself with the terminal type `xterm-ghostty`,
///     which could cause problems for remote machines where Ghostty's _terminfo files_
///     are not installed. Many programs rely on terminfo files to know what the
///     terminal is capable of, and may crash with "unknown terminal type" errors when
///     the terminfo files are absent or exhibit strange behavior.
///
///     When `term-only` is set, for remote connections Ghostty would instead identify
///     itself as `xterm-256color`, which is a compatibility mode understood in most
///     systems.
///
///     This option is best used when you need to connect to a wide variety of remote
///     devices, some of which you might not have access to.
```

Similarly, error messages should be specific and actionable. Instead of vague messages like "your compositor does not support the protocol", provide specific guidance such as "your distro's gtk4-layer-shell version is defective; update to 1.0.4 or later".