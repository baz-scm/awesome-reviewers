---
title: Bound traversal algorithms safely
description: When writing an algorithm that recursively or iteratively walks a self-referential
  or unbounded structure (symlink chains, directory trees, nested references), explicitly
  guard against cycles and cap total work, instead of assuming the input is well-formed.
  A link or reference that loops back to a directory already being expanded (itself,
  an ancestor, or a...
repository: cline/cline#zzz-unlikely-123abc
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 71035
---

When writing an algorithm that recursively or iteratively walks a self-referential or unbounded structure (symlink chains, directory trees, nested references), explicitly guard against cycles and cap total work, instead of assuming the input is well-formed. A link or reference that loops back to a directory already being expanded (itself, an ancestor, or a sibling pointing back) must be detected and skipped rather than re-expanded, and the total number of expansions should have a hard ceiling so a small malicious or accidental cycle cannot blow up into exponential work. Cover this with a regression test that constructs the pathological case (e.g., dozens of symlinks looping back to `.` or `..`) and asserts it still completes quickly and only copies real content.

The same discipline applies to lower-level sequence algorithms: operate on the real unit boundaries of the data rather than a convenient but incorrect approximation. For example, truncating a string by raw character offset can split a UTF-16 surrogate pair and produce an invalid string — use a surrogate-aware slice helper everywhere a string is cut, including in any secondary truncation pass the data might go through later. Likewise, a fuzzy/partial match (e.g., substring-based diff matching) should require a minimally meaningful match length so trivial or single-character substrings don't produce false positives.

In short: before shipping an algorithm over a structure that could contain cycles, unbounded size, or multi-unit encodings, ask "what's the worst-case/pathological input?" and add an explicit bound, cycle check, or boundary-aware operation plus a test that exercises it.</description>
</invoke>
