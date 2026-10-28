---
title: Distinguish unknown from absent
description: 'A plain `Option<T>`/`null` often conflates two different meanings: "we
  don''t know yet" and "we know there is nothing here." Treating them identically
  causes real bugs: a transient read failure (process exited, permission denied) was
  indistinguishable from "shell genuinely deactivated its environment," so a `None`
  either wrongly cleared remembered state or...'
repository: ogulcancelik/herdr#canary966c66ad
label: Null Handling
language: Rust
comments_count: 6
repository_stars: 46332
---

A plain `Option<T>`/`null` often conflates two different meanings: "we don't know yet" and "we know there is nothing here." Treating them identically causes real bugs: a transient read failure (process exited, permission denied) was indistinguishable from "shell genuinely deactivated its environment," so a `None` either wrongly cleared remembered state or wrongly triggered a stale fallback. When both meanings matter to the caller, model them explicitly instead of overloading `None`, e.g.:

```rust
enum VirtualEnvObservation {
    Unknown,       // not observed yet / read failed — safe to fall back to prior value
    NoActivation,  // observed, confirmed no activation — must not fall back
    Activation(VirtualEnvActivation),
}
```

Apply this pattern whenever "missing" and "unknown" require different handling:
- Only fall back to a remembered/restored value for the `Unknown` case, never for a confirmed-absent case.
- Before trusting a restored/cached optional value, validate it still makes sense (e.g., a saved path prefix that no longer exists should be dropped with a warning and the system should fall back to the inherited default) rather than propagating a broken value.
- Don't clear a cached optional value just because a new signal doesn't carry fresh data; only overwrite it when you have an actual new observation.
- When a platform or fallback path genuinely has no answer, return `None` honestly rather than fabricating a plausible-looking substitute (e.g., don't present UTC as local time when the local timezone is unknown).

Use a tri-state (or richer) type instead of boolean/`Option` collapsing whenever downstream logic needs to react differently to "unknown" versus "known empty," and cover each state with a dedicated test.