---
title: Verify documented behavior
description: Documentation must describe what the product actually does, not what
  it was intended to do, used to do, or is assumed to do. Before writing or updating
  a doc, verify claims against the source code, CLI help output, or direct testing
  (e.g. `lsof`, reading the implementing script) rather than carrying forward old
  wording. When a verified check reveals a...
repository: cline/cline?foo=bar
label: Documentation
language: Other
comments_count: 9
repository_stars: 71082
---

Documentation must describe what the product actually does, not what it was intended to do, used to do, or is assumed to do. Before writing or updating a doc, verify claims against the source code, CLI help output, or direct testing (e.g. `lsof`, reading the implementing script) rather than carrying forward old wording. When a verified check reveals a mismatch between docs and behavior — a wrong default (`--retries` documented as 6 while `main.ts` applies `args.retries ?? 3`), a flag that does nothing (`CLINE_HOOKS_DIR`), or an overclaim of what's guaranteed ("enforces" vs. "supports" when a user can still edit local files between sessions) — fix whichever side is wrong: update the doc to match the code, or file/link an issue and fix the code, rather than leaving both to quietly disagree.

Avoid documenting broken, deprecated, or non-functional behavior as if it were normal. If a feature is being removed or no longer works anywhere, prefer deleting the doc (or the feature) over describing it with the caveat "currently broken" — that phrasing implies it will be fixed soon and invites misuse. Reserve caveats for cases that are large, ongoing efforts where removal isn't practical yet.

When behavior varies by build, platform, or provider (e.g., which log file a client writes, which tools a model provider executes itself, how a config key is derived per build), state the specific cases explicitly and verify each one individually rather than generalizing from a single observation or listing an assumed-exhaustive set.