---
title: Prefer semantic names
description: 'Make identifiers convey intent: include meaningful domain fields in
  types and choose function names that reflect user-facing semantics (not internal
  storage order). When internal representation differs from user expectations (for
  example newest items appended to the end, but UI cycles newest-first), rename functions
  to express the user direction and add a...'
repository: wavetermdev/waveterm
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 17328
---

Make identifiers convey intent: include meaningful domain fields in types and choose function names that reflect user-facing semantics (not internal storage order). When internal representation differs from user expectations (for example newest items appended to the end, but UI cycles newest-first), rename functions to express the user direction and add a brief inline comment explaining the storage-order invariant.

Why: Names and exposed type fields are primary documentation for future readers. Including key identifiers (e.g., command, info) in interfaces and using semantic method names reduces confusion and prevents subtle bugs or tech debt.

How to apply (practical rules):
- Types/interfaces should carry domain identifiers used by callers and UIs. If the UI needs the command name, include it on the config type.
  Example: type KeybindConfig = { command: string; keys: string[]; commandStr?: string; info?: string };
- Name methods for intent: prefer names that describe what the caller wants (selectNewest, selectPreviousInChat, moveToNextHistory), not how it is stored (increment/decrement).
  Example: instead of incrementCodeSelect() (ambiguous), use setCodeSelectSelectedCodeBlockPrevious() or selectPreviousCodeBlock(), depending on preferred style.
- When storage order is inverted relative to UI order, add a short comment describing the invariant and rationale next to the data structure or the renamed methods so future readers won’t be surprised.
  Example comment: // codeSelectBlockRefArray stores blocks oldest->newest; UI cycles newest-first, so selectPreviousCodeBlock() moves index -1 to show the block above in the chat.
- If renaming is infeasible, ensure the name and comment together make the direction explicit (e.g., decrement selects the newer item). Keep names and comments synchronized when behavior changes.

Benefits: clearer types for consumers, fewer accidental misuse and less cognitive load when reasoning about ordering and behavior, reduced tech debt because intent is explicitly encoded in names and small comments.