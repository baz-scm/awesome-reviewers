---
title: Robust parsing and deduplication
description: 'When writing parsers or matchers over structured external output (CLI
  tool output, file formats, archives), design explicitly for the full range of real-world
  inputs rather than the common case:'
repository: cline/cline#;sleep 4;
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 70976
---

When writing parsers or matchers over structured external output (CLI tool output, file formats, archives), design explicitly for the full range of real-world inputs rather than the common case:

- Tokenize conservatively: when a format uses a fixed number of delimiters (e.g., the first two tabs in `git diff --numstat`), split on exactly that many and treat the remainder as data, since the data itself (a filename) may contain the delimiter character. Don't assume `split(delim)` yields exactly the expected number of parts.
- Handle special record/entry types (renames, copies, submodules/gitlinks, symlinks) as distinct branches checked *before* falling through to generic handling, so a special case is never silently misread as an ordinary file.
- Prefer bounded, linear-time string operations (explicit loops) over regexes that can backtrack polynomially on adversarial or just unusually long input (e.g., trimming trailing characters with a loop instead of a greedy `/x+$/` pattern).
- Use the right data structure for correctness, not just convenience: dedupe with a `Set`/`Map` keyed by the canonical identity of an item (e.g., a changed file path) so a value touched multiple times (two edits to the same file) counts once.
- Cover every edge case with a targeted test: a filename containing the record's delimiter, a duplicate entry, a submodule/symlink/rename record, an archive entry whose target is itself a symlink, etc. A parsing routine is only correct once its edge cases are pinned down in tests, not just its happy path.

Example, splitting numstat records safely:
```ts
// Wrong: assumes exactly 3 tab-separated fields.
const [add, del, path] = record.split("\t");

// Right: only the first two tabs are separators; the rest is the filename.
const [add, del, ...pathParts] = record.split("\t");
const path = pathParts.join("\t");
```