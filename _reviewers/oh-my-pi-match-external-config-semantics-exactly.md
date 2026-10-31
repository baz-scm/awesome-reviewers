---
title: Match external config semantics exactly
description: 'When reading, writing, or transferring configuration governed by an
  external format or tool (e.g. git''s config files), replicate that tool''s full
  semantics rather than the common-case behavior, and cover each semantic edge case
  with a dedicated test. Config-file parsing has subtle rules that are easy to miss
  on a first pass: repeated keys must resolve using...'
repository: can1357/oh-my-pi
label: Configurations
language: Rust
comments_count: 5
repository_stars: 37317
---

When reading, writing, or transferring configuration governed by an external format or tool (e.g. git's config files), replicate that tool's full semantics rather than the common-case behavior, and cover each semantic edge case with a dedicated test. Config-file parsing has subtle rules that are easy to miss on a first pass: repeated keys must resolve using the tool's own precedence (e.g. "last assignment wins" for git's scalar keys, not "first match"), escaping/quoting rules must be applied uniformly and exactly as the source tool defines them (git decodes `\\`, `\"`, `\n`, `\t`, `\b` regardless of quoting, with quoting only affecting whether whitespace/comment characters are literal), and encoding artifacts such as a leading UTF-8 BOM must be stripped exactly as the authoritative parser does. Similarly, when code copies, detaches, or otherwise transfers a configuration-bearing structure (e.g. splitting a submodule's git directory from its superproject), ensure *every* relevant config file is carried over — not just the primary one (e.g. `config` but also `config.worktree`, or remote/branch settings) — so no setting is silently dropped. Each of these edge cases should land with its own named regression test (e.g. `core_worktree_repeated_key_honors_last_occurrence`, `core_worktree_decodes_unquoted_escapes`, `core_worktree_skips_a_leading_utf8_bom`) so future refactors can't reintroduce the gap.