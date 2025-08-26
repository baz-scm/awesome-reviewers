---
title: Document configuration choices
description: Add explanatory comments for non-obvious configuration settings, especially
  when they deviate from defaults or serve specific purposes. Configuration choices
  that aren't immediately clear should include comments explaining their rationale,
  impact, or relationship to other settings.
repository: semgrep/semgrep
label: Configurations
language: Other
comments_count: 4
repository_stars: 12598
---

Add explanatory comments for non-obvious configuration settings, especially when they deviate from defaults or serve specific purposes. Configuration choices that aren't immediately clear should include comments explaining their rationale, impact, or relationship to other settings.

This helps prevent accidental changes, aids debugging, and makes maintenance easier for future developers who need to understand why specific settings exist.

Examples of when to add configuration documentation:
- Special repository settings: `# Need beta repo for OCaml 5.0 compatibility`
- Environment-specific endpoints: `# Use dev endpoint during development phase`
- Dependency coupling: `# Keep in sync with requirements.txt when adding Python deps`
- Non-standard defaults: `# Skip crypto libs to reduce log noise`

```ocaml
(* Default libraries to skip in logging - you can use regexps *)
let default_skip_libs = [
  "cohttp.lwt.client";
  "dns*";  (* Skip all DNS-related logging *)
]
```

The comment should explain both what the configuration does and why it's necessary, making the codebase more maintainable and reducing the likelihood of configuration-related bugs.