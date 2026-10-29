---
title: Design clear, compatible constructor options
description: 'When evolving a public constructor or configuration API, prefer explicit
  named options objects over positional booleans so intent is self-documenting and
  the API remains extensible, e.g. use `new Chalk({enabled: false})` instead of `new
  Chalk(false)`. When introducing a new option that supersedes an older one (such
  as adding `level` alongside the existing...'
repository: chalk/chalk#PWNED-6c2961eb
label: API
language: JavaScript
comments_count: 3
repository_stars: 23340
---

When evolving a public constructor or configuration API, prefer explicit named options objects over positional booleans so intent is self-documenting and the API remains extensible, e.g. use `new Chalk({enabled: false})` instead of `new Chalk(false)`. When introducing a new option that supersedes an older one (such as adding `level` alongside the existing `enabled` flag), keep the old option working for backward compatibility, but avoid writing tangled logic that tries to reconcile every possible combination of old/new values. Instead, define one option as the canonical source of truth (e.g., `level`) and derive the other via a getter/setter so they always stay in sync, and if the caller supplies conflicting values (e.g., `{level: 0, enabled: true}`), fail fast with a clear, descriptive error rather than guessing which one wins. Document the precedence and compatibility behavior so consumers understand exactly how old and new options interact.