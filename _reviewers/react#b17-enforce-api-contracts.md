---
title: Enforce API Contracts
description: When designing or modeling an API surface, ensure it (1) exactly matches
  the real contract at call boundaries (parameter count/placement), and (2) prevents
  invalid states by construction (hide internal representations that can be misused;
  expose invariant-preserving constructors and safe views).
repository: facebook/react#b17
label: API
language: Rust
comments_count: 2
repository_stars: 251891
---

When designing or modeling an API surface, ensure it (1) exactly matches the real contract at call boundaries (parameter count/placement), and (2) prevents invalid states by construction (hide internal representations that can be misused; expose invariant-preserving constructors and safe views).

Application:
- Signature/parameter placement: verify against the underlying API so options belong in the correct method call.
  - Example rule: if an API takes only `new(callback)`, don’t model additional “constructor options”; move them to the call that accepts options (e.g., `observe(target, options)`).
- Invariants in public types: avoid exposing a public constructible representation that allows breaking required invariants.
  - Prefer: `pub fn from_code_units(...)` (canonicalizes) + `pub fn view(&self) -> JsStringRef<'_>` (borrowed read-only view).

Illustrative pattern:
```rust
pub struct JsString(Repr); // Repr is kept private

enum Repr {
    Utf8(String),
    Wtf16(Vec<u16>), // must satisfy the unpaired-surrogate invariant
}

pub enum JsStringRef<'a> {
    Utf8(&'a str),
    Wtf16(&'a [u16]),
}

impl JsString {
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize and enforce invariants here
        # unimplemented!()
    }

    pub fn view(&self) -> JsStringRef<'_> {
        // provide a safe, read-only view
        # unimplemented!()
    }
}
```