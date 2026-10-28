---
title: Fail closed on ambiguity
description: 'When a security-relevant check—identity, ownership, permission, capability,
  or allowed state—cannot be conclusively verified, treat the ambiguous case as unauthorized/unsafe
  rather than assuming it is benign. Concretely:'
repository: ogulcancelik/herdr#canary966c66ad
label: Security
language: Rust
comments_count: 9
repository_stars: 46332
---

When a security-relevant check—identity, ownership, permission, capability, or allowed state—cannot be conclusively verified, treat the ambiguous case as unauthorized/unsafe rather than assuming it is benign. Concretely:

- Do not widen a fallback or exception condition beyond what is proven necessary. Match only the exact error/condition known to correspond to the safe case (e.g. a specific `io::ErrorKind`), not "similar" ones added defensively, since that silently broadens what gets treated as safe.
- A failed lookup/query is not proof that a resource belongs to someone else or is irrelevant; absence of proof of danger is not proof of safety. Keep enumeration/validation fail-closed when identity cannot be established.
- Re-verify identity or permission state immediately before acting, especially across any check-then-use gap (TOCTOU): re-sample ownership/sequence numbers after an operation that could change them, confirm a file's identity before deleting it or trusting a leftover marker, and only unlink/replace resources whose identity still matches what was bound/created.
- When negotiating behavior with a peer of unknown or older capability (e.g. protocol/version compatibility), keep the more restrictive/protective behavior by default and only relax it when the peer explicitly advertises support for the safer alternative.
- Prefer rejecting or failing startup with actionable guidance over silently degrading protection (e.g. accepting a group/world-readable directory, or accepting an unverifiable bundle) just to keep an edge case working.
- Gate sensitive command dispatch explicitly (deny-by-default allowlists) instead of including a sensitive subcommand in a shared/unconditional list that other platforms can reach unintentionally.

Example pattern: a Unix socket permission fallback should match exactly the error kind proven to mean "this filesystem cannot chmod sockets," should only tighten directories inside the application's own managed config tree, and should fail loudly with remediation guidance for externally supplied paths rather than quietly leaving them group/world accessible.