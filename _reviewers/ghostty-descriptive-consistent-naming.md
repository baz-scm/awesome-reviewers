---
title: Descriptive consistent naming
description: Use descriptive, consistent naming that follows language and platform
  conventions. Choose names that clearly communicate purpose and context, and maintain
  consistency across similar elements.
repository: ghostty-org/ghostty
label: Naming Conventions
language: Other
comments_count: 13
repository_stars: 32864
---

Use descriptive, consistent naming that follows language and platform conventions. Choose names that clearly communicate purpose and context, and maintain consistency across similar elements.

For variables:
- Replace single-letter variables with descriptive names: 
  ```diff
  - local e=() o=() c=()
  + local env=() opts=() ctrl=()
  ```
- Add prefixes to indicate context or purpose:
  ```diff
  - local env=() opts=() ctrl=()
  + local ssh_env=() ssh_opts=() ssh_ctrl=()
  ```
- Follow language-specific conventions (Zig uses camelCase for functions, snake_case for variables):
  ```diff
  - pub fn wait_xev(
  + pub fn waitXev(
  
  - pub fn resourcesDir(alloc: Allocator, hostAccessible: bool)
  + pub fn resourcesDir(alloc: Allocator, host_accessible: bool)
  ```
- Use lowercase for enum values unless there's a reason not to:
  ```diff
  - pub const SetTitleSource = enum { USER, TERMINAL };
  + pub const SetTitleSource = enum { user, terminal };
  ```
- Use singular forms for type names:
  ```diff
  - pub const Dirs = enum {
  + pub const Dir = enum {
  ```
- Follow standard acronym casing conventions:
  ```diff
  - const updated = fixZHLocale(locale);
  + const updated = fixZhLocale(locale);
  ```

For APIs and actions:
- Use consistent naming patterns for related functionality:
  ```diff
  - .{ "command-palette", gtkActionToggleCommandPalette },
  + .{ "toggle-command-palette", gtkActionToggleCommandPalette },
  ```
- Choose names that match established terminology:
  ```diff
  - GHOSTTY_ACTION_BELL,
  + GHOSTTY_ACTION_RING_BELL,
  ```
- Use semantic names that match protocols or standards:
  ```diff
  - true,
  + none,
  ```

Choose names that balance brevity with clarity, and consider how names will be interpreted by other developers.