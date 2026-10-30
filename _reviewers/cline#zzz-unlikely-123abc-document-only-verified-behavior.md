---
title: Document only verified behavior
description: Documentation must reflect what the product actually does, not aspirational
  or historical behavior. If a feature, flag, or environment variable is broken, deprecated,
  or silently ignored, don't document it as if it works — either fix the underlying
  behavior or remove the documentation entirely rather than leaving a misleading entry
  (e.g., listing...
repository: cline/cline#zzz-unlikely-123abc
label: Documentation
language: Other
comments_count: 5
repository_stars: 71035
---

Documentation must reflect what the product actually does, not aspirational or historical behavior. If a feature, flag, or environment variable is broken, deprecated, or silently ignored, don't document it as if it works — either fix the underlying behavior or remove the documentation entirely rather than leaving a misleading entry (e.g., listing `CLINE_HOOKS_DIR` as "additional hooks directory" when it currently has no effect, or describing a `.clineignore` filter that isn't actually enforced). Documenting broken functionality invites users to rely on it and makes the docs look careless.

Before publishing, verify every command, flag, and example by actually running it: an example like `cline connect telegram --restart -k <BOT-TOKEN>` must be checked against real argument parsing, since putting an option after the subcommand name can silently fail even though it reads correctly. If an option is accepted but has no real effect (e.g., `--limit` not behaving as described), fix the behavior or drop it from the reference table rather than documenting the broken state.

When a genuine limitation or caveat must be kept (because fixing it is out of scope or complex), state it completely and practically — tell the reader concretely which situations it affects and how to recognize them, rather than a vague aside like "providers that run tools themselves" without naming the class of providers or giving the user a way to check. Reserve "known limitation" language for cases where the fix is actually in progress; otherwise, remove the stale content.