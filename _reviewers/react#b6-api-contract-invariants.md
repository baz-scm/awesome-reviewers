---
title: API Contract & Invariants
description: When exposing or modeling an API boundary, ensure (1) the modeled call
  signature matches the real contract and (2) any represented protocol invariants
  are enforced by the public type surface.
repository: facebook/react#b6
label: API
language: Rust
comments_count: 2
repository_stars: 251888
---

When exposing or modeling an API boundary, ensure (1) the modeled call signature matches the real contract and (2) any represented protocol invariants are enforced by the public type surface.

Apply:
- API surface accuracy: confirm which parameters belong to a constructor vs a subsequent method (don’t copy shapes between similar JS APIs).
- Invariant-safe types: don’t make a representation publicly constructible if it can violate required invariants; instead, keep the representation private and expose safe constructors plus borrowed view/ref types.

Example (invariant-safe API surface):
```rust
// Keep representation private so callers cannot construct invalid states.
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
    // Canonicalizing constructor (enforces invariants)
    pub fn from_code_units(u: &[u16]) -> Self { /* canonicalizes */ }

    // Borrowed view (prevents invalid construction)
    pub fn view(&self) -> JsStringRef<'_> { /* &self → borrowed view */ }
}
```

Checklist:
- Does every parameter/option location match the real external API contract?
- Can any public type be directly constructed into an invalid/undefined representation state?
- Are callers guided toward safe constructors and read-only views at the boundary?