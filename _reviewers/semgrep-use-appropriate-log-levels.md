---
title: Use appropriate log levels
description: Choose log levels based on the intended audience to prevent user-visible
  noise. Most logging should use `Logs.debug` rather than `Logs.info` or `Logs.err`,
  since info-level and above messages are visible to end users with `--verbose` or
  by default.
repository: semgrep/semgrep
label: Logging
language: Other
comments_count: 4
repository_stars: 12598
---

Choose log levels based on the intended audience to prevent user-visible noise. Most logging should use `Logs.debug` rather than `Logs.info` or `Logs.err`, since info-level and above messages are visible to end users with `--verbose` or by default.

**Guidelines:**
- Use `Logs.debug` for development/troubleshooting information (parser errors, internal state, performance details)
- Use `Logs.info` only for information that end users should see with `--verbose` 
- Use `Logs.err` only for errors that end users need to act upon
- Tagged messages (with `~tags`) should generally be debug-level unless specifically intended for users

**Example:**
```ocaml
(* Bad - creates noise for users *)
Logs.err (fun m -> m ~tags "BUG PARSING LOCAL DECL PROBABLY");
Logs.info (fun m -> m "skipping: %s" (Tok.content_of_tok tok));

(* Good - appropriate for debugging *)  
Logs.debug (fun m -> m ~tags "BUG PARSING LOCAL DECL PROBABLY");
Logs.debug (fun m -> m "skipping: %s" (Tok.content_of_tok tok));
```

The principle is that no log message should appear to command-line users unless they explicitly enable debugging or the message requires user action.