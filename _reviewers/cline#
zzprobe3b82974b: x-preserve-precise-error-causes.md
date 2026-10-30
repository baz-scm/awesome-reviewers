---
title: Preserve precise error causes
description: When catching, wrapping, or classifying a failure, keep the distinction
  between genuinely different causes instead of collapsing them into one generic bucket.
  A caller, a user-facing message, a retry decision, or telemetry dimension is often
  built on *which* error occurred, so losing that signal silently breaks correctness
  even though the code "handles" the...
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Error Handling
language: TypeScript
comments_count: 12
repository_stars: 71067
---

When catching, wrapping, or classifying a failure, keep the distinction between genuinely different causes instead of collapsing them into one generic bucket. A caller, a user-facing message, a retry decision, or telemetry dimension is often built on *which* error occurred, so losing that signal silently breaks correctness even though the code "handles" the error.

Concretely:
- When re-throwing or wrapping an error, attribute it to the stage that actually produced it, not the stage that happened to observe it. For example, a read failure inside a write pipeline should surface as a read error, not get folded into `WRITE_FAILED` just because the catch block is on the write path.
- When mapping a status code, exit code, or error string to a semantic outcome (e.g. "not a repository", "session not found", "file missing"), match the narrowest condition that is actually true, and let anything else fall through as a distinct/unknown failure rather than assuming the common case. A `git` exit 128 means "not a repository" only when stderr says so; any other fatal error must not be reported as a clean/empty state.
- Don't let a fallback path discard diagnostic specificity: if a lookup fails for one well-understood reason (missing credential, unmatched provider, stale fixture) versus another (network error, malformed input), preserve that distinction all the way to the message or telemetry field consuming it, instead of defaulting both to the same generic outcome.
- Carry structured error information (e.g. a captured timeout object, an original exception) through async boundaries and serialization layers rather than re-deriving it from a lossy string later; check for the already-captured cause before falling back to a weaker signal.
- Guard every place that derives a result status from a sub-call's outcome: check the actual failure/finish reason of a downstream operation before reporting success, rather than hardcoding an optimistic status.

A simple rule of thumb: before writing a catch block or a classification function, ask "does this distinguish every case a caller needs to react to differently?" If two meaningfully different failures would produce the same error code, message, or status, that's a bug waiting to surface as a wrong user-facing message, a bad retry decision, or misleading telemetry.