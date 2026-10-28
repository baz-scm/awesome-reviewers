---
title: CLI subcommand surface consistency
description: When adding or modifying CLI (or API) subcommands, keep each command's
  argument surface scoped strictly to that command and keep its displayed usage in
  sync with its actual validation rules. Do not copy flags between subcommands just
  because they look similar — e.g. adding `--no-focus` to `worktree remove` because
  it exists on `worktree open` creates...
repository: ogulcancelik/herdr#canary966c66ad
label: API
language: Rust
comments_count: 3
repository_stars: 46332
---

When adding or modifying CLI (or API) subcommands, keep each command's argument surface scoped strictly to that command and keep its displayed usage in sync with its actual validation rules. Do not copy flags between subcommands just because they look similar — e.g. adding `--no-focus` to `worktree remove` because it exists on `worktree open` creates unrelated, unintended API surface and breaks compatibility expectations. Instead, add only the flags/options a given subcommand genuinely supports, and verify existing callers/docs/tests to confirm the current contract before changing it.

When arguments are mutually exclusive or form a required group (e.g. `--path` vs `--branch` for `worktree open`), declare that as a single required group so the generated help/synopsis (e.g. `(--path PATH | --branch NAME)`) and the runtime validation enforce the exact same rule — never let the two drift apart.

Finally, when a command family carries cross-cutting behavior contracts (e.g. remote dispatch, path resolution), new commands must either explicitly opt into the existing contract or be deliberately excluded with a clear comment explaining why (e.g. "registry commands are not remote-forwardable; if remote support is added later it must adopt the existing `remote_path_is_absolute` contract"). Avoid silently relying on assumptions that may not hold as the command set grows.