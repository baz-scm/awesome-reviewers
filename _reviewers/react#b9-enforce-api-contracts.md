---
title: Enforce API Contracts
description: When designing or modeling an API boundary (external platform types or
  public Rust types that represent JS/wire data), ensure (1) the signature/parameter
  semantics exactly match the true contract, and (2) the public surface prevents creation
  of invalid states.
repository: facebook/react#b9
label: API
language: Rust
comments_count: 2
repository_stars: 251891
---

When designing or modeling an API boundary (external platform types or public Rust types that represent JS/wire data), ensure (1) the signature/parameter semantics exactly match the true contract, and (2) the public surface prevents creation of invalid states.

Practical rules:
- Don’t assume “similar types” share the same constructor shape. Verify arity and where options belong (e.g., constructor vs. `observe(target, options)`).
- Avoid exposing raw representations that callers can construct into invalid states. Keep canonical constructors/invariants internal, and expose safe borrowed views/refs for read-only access.

Example pattern (Rust invariants via refs):
```rust
// Internals enforce canonicalization/invariants.
pub struct JsString(Repr);

enum Repr {
    Utf8(String),
    Wtf16(Vec<u16>),
}

pub enum JsStringRef<'a> {
    Utf8(&'a str),
    Wtf16(&'a [u16]),
}

impl JsString {
    // Only constructor(s) that enforce the invariant.
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize + enforce unpaired-surrogate rules
        /* ... */
    }

    // Safe borrowed view for callers.
    pub fn view(&self) -> JsStringRef<'_> {
        /* ... */
    }
}
```

Use the same “boundary discipline” for API modeling code: confirm parameter counts and meanings against the real spec before hardcoding the interface in your globals/wrappers.