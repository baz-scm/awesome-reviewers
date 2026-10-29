---
title: Guard security state transitions
description: When code crosses a security boundary (e.g., upgrading a connection to
  TLS via STARTTLS, or recovering from an error during a filesystem operation), explicitly
  discard or re-validate any state that could have been influenced by an attacker
  before the boundary was crossed. Buffered plaintext data, cached untagged responses,
  file descriptors, or paths...
repository: python/cpython
label: Security
language: Python
comments_count: 3
repository_stars: 77696
---

When code crosses a security boundary (e.g., upgrading a connection to TLS via STARTTLS, or recovering from an error during a filesystem operation), explicitly discard or re-validate any state that could have been influenced by an attacker before the boundary was crossed. Buffered plaintext data, cached untagged responses, file descriptors, or paths resolved before the transition must never be trusted or reused afterward, since an attacker can inject data or swap a directory for a symlink (TOCTOU) in that window. For example, after a successful STARTTLS handshake, clear all pre-TLS read buffers and any cached protocol state (not just the socket buffer) so injected commands cannot be replayed as if they arrived over the encrypted channel. Similarly, when recovering from a `PermissionError` during recursive directory cleanup, re-check that a path still refers to the expected type (not a newly-created symlink) before performing privileged operations like `chmod`, and only act if the path still exists in its expected form. Any fix for this class of vulnerability must include a regression test that reproduces the race or injection scenario (as done for the STARTTLS buffer flush and the CVE-2026-12345 symlink-race test), and the test should cover all relevant protocol/version variants (e.g., both TLS 1.2 and 1.3, including session-resumption paths) to ensure the fix isn't accidentally narrow.</description>
</invoke>
