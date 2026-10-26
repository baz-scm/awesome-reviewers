---
title: Preserve API Contracts
description: When designing or modeling client/bridge APIs, ensure (1) the interface
  shape matches the underlying contract, and (2) any exposed types cannot be constructed
  into invalid states.
repository: facebook/react#b2
label: API
language: Rust
comments_count: 2
repository_stars: 251882
---

When designing or modeling client/bridge APIs, ensure (1) the interface shape matches the underlying contract, and (2) any exposed types cannot be constructed into invalid states.

- Match parameter placement exactly: verify which arguments belong to a constructor vs a later method call (e.g., options passed to `observe(...)` belong there, not to the `ResizeObserver` constructor).
- Enforce invariants via the public surface: don’t expose a representation that allows callers to bypass required invariants. Prefer a private internal `Repr`, safe constructors that canonicalize/validate, and borrowed “view/ref” accessors.

Example pattern (Rust):
```rust
pub struct JsString(Repr);

enum Repr {
    Utf8(String),
    Wtf16(Vec<u16>), // invariant: represents the marked/unpaired-surrogate encoding
}

pub enum JsStringRef<'a> {
    Utf8(&'a str),
    Wtf16(&'a [u16]),
}

impl JsString {
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize/validate to maintain invariant
        unimplemented!()
    }

    pub fn view(&self) -> JsStringRef<'_> {
        // provide borrowed access without allowing invalid construction
        unimplemented!()
    }
}
```

Apply this standard to REST/GraphQL schema modeling, SDK method signatures, and any language-bridge “globals” so the API is both correct in shape and safe in state.