---
title: Deterministic Grammar Changes
description: 'When updating diagram parsers (Jison/Langium/Chevrotain), treat lexer/tokenization
  precedence as a compatibility contract: ensure changes don’t break existing inputs
  and that intended tokens are unambiguously chosen.'
repository: mermaid-js/mermaid
label: Algorithms
language: Other
comments_count: 5
repository_stars: 87952
---

When updating diagram parsers (Jison/Langium/Chevrotain), treat lexer/tokenization precedence as a compatibility contract: ensure changes don’t break existing inputs and that intended tokens are unambiguously chosen.

Apply these rules:
1) Assume the first/earliest matching token wins (Langium/Chevrotain behavior). Avoid overlapping regex/patterns that allow one token to “shadow” others. If overlap is unavoidable, control it explicitly (tighten patterns, reorder tokens, or use a custom matcher that refuses matches that should belong to other token types).
2) Never change the meaning of a previously-supported character/string without explicitly preserving the old interpretation (or providing a migration plan). If a symbol like `-` previously parsed as a generic/node string, keep that option working while adding the new operator token.
3) If you remove/replace lexer terminals to resolve conflicts, confirm that downstream validation preserves the same semantics the feature provided (don’t silently drop behavior).
4) Add regression tests for prior real-world diagrams/labels that previously worked—especially cases involving punctuation, quotes, and ambiguous terminals.

Example (conceptual fix for “shadowing”):
- Instead of defining a broad token that can match everything, define a narrower token or use a matcher that checks the input context before returning the token.

In code review, ask: “What token now matches this substring, and does that substring still parse the same way as before? Which token wins, and why?”