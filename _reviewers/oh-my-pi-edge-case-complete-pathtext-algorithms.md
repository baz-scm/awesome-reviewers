---
title: Edge-case-complete path/text algorithms
description: When an algorithm walks a filesystem tree or parses structured text (e.g.
  resolving `.git` pointer targets, classifying nested repositories, or parsing git-config),
  base every decision on the actual underlying mechanism rather than a proxy signal,
  and enumerate the real-world edge cases the mechanism allows before calling the
  logic complete.
repository: can1357/oh-my-pi
label: Algorithms
language: Rust
comments_count: 9
repository_stars: 37317
---

When an algorithm walks a filesystem tree or parses structured text (e.g. resolving `.git` pointer targets, classifying nested repositories, or parsing git-config), base every decision on the actual underlying mechanism rather than a proxy signal, and enumerate the real-world edge cases the mechanism allows before calling the logic complete.

Concretely:
- Resolve relative references against the directory they were actually written in/for, not against a convenient substitute (e.g. a submodule's or worktree's relative `gitdir:`/`commondir` pointer must resolve against the source checkout, not the copy, or it silently targets the wrong tree).
- Classify entities by what they structurally are (e.g. read `commondir` to tell a linked-worktree admin dir from a real repository) instead of inferring from path shape or naming convention, since legitimate inputs can look like the thing they are not (a submodule path containing `worktrees` or `modules`).
- Don't gate a safety check on an unrelated proxy measurement. If the actual failure mode (e.g. unbounded recursion when a destination lands inside its source) is independent of some other property (e.g. filesystem reflink support), the check must cover the failure mode directly on every input, not only where the proxy happens to agree.
- Account for every variant the format/spec permits: symlinked indirections, bind-mounted/aliased paths, split-index sibling files, quoted vs. unquoted values, comments after a section header, case-insensitive keys, backslash escapes, and line continuations are all legitimate inputs that a "happy path" implementation will otherwise silently mishandle.
- For every edge case discovered during review, add a focused regression test that fails without the fix and passes with it, so the specific scenario (not just the general code path) stays covered.

Example: a config-value decoder must not assume quoting implies escaping — `worktree = ../sub\"quote` is valid unquoted-with-escape syntax — and must track quote state across a backslash line continuation, joining `ma\` + `in` into `main` exactly as the real parser would, rather than truncating at the line boundary.

Treat any discussion comment that says "not done in this round" or "still open" as a signal that the edge-case enumeration is incomplete; the standard is not satisfied until the missed case has an identified fix and a regression test, not merely a description of the gap.