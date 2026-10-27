---
title: Semantics-safe Public APIs
description: When designing or modeling an API boundary, ensure (1) the exposed shape
  matches the real underlying semantics, and (2) the public surface cannot represent
  invalid states.
repository: facebook/react#b15
label: API
language: Rust
comments_count: 2
repository_stars: 251891
---

When designing or modeling an API boundary, ensure (1) the exposed shape matches the real underlying semantics, and (2) the public surface cannot represent invalid states.

Apply this in two common situations:

1) Signature/parameter correctness
- Verify constructor/method arity and parameter meaning against the real API (and avoid copy/paste from a related API).
- Ensure equivalent representations are consistent across languages (e.g., TS and Rust globals).

2) Invariant-preserving types
- Don’t expose public types that let callers construct values that violate required invariants.
- Prefer a private/internal representation plus safe constructors, and provide borrowed “view/ref” types for access.

Example pattern (safe view/ref for an invariant-carrying value):
```rust
pub struct JsString(Repr); // Repr is private

enum Repr {
    Utf8(String),
    Wtf16(Vec<u16>),
}

pub enum JsStringRef<'a> {
    Utf8(&'a str),
    Wtf16(&'a [u16]),
}

impl JsString {
    // Canonicalizes/enforces invariants
    pub fn from_code_units(u: &[u16]) -> Self { /* canonicalizes */ }

    // Borrowed access for inspection
    pub fn view(&self) -> JsStringRef<'_> { /* &self -> JsStringRef */ }
}
```
Use this standard to prevent subtle API mismatches and to keep invariants enforceable at the boundary.