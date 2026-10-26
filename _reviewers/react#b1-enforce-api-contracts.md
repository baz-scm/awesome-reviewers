---
title: Enforce API Contracts
description: When exposing or modeling an API surface (web globals, wrappers, or public
  data types), ensure your code preserves the real contract and prevents invalid states.
repository: facebook/react#b1
label: API
language: Rust
comments_count: 2
repository_stars: 251878
---

When exposing or modeling an API surface (web globals, wrappers, or public data types), ensure your code preserves the real contract and prevents invalid states.

Apply this:
- Contract fidelity: verify constructor/function signatures and parameter meanings against the source API. Don’t copy shapes from similar APIs unless semantics match.
- Invariant encapsulation: if a type must maintain an internal safety invariant (e.g., a representation must be normalized/canonical), do not expose a representation that callers can construct into an invalid state. Prefer private internal representation, controlled constructors, and “view”/borrowed reference types.

Example patterns:
```rust
// Contract fidelity: model ResizeObserver with only the callback constructor param.
// (Options belong on observe(target, options), not on construction.)
let resize_observer_ctor = add_function(
    shapes,
    Vec::new(),
    FunctionSignatureBuilder {
        positional_params: vec![Effect::Freeze, Effect::Read],
        // ...
    },
);

// Invariant encapsulation: keep internal repr private; expose a borrowed view.
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
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize/validate to preserve invariant
        // ...
        # unimplemented!()
    }

    pub fn view(&self) -> JsStringRef<'_> {
        // borrowed, invariant-preserving view
        # unimplemented!()
    }
}
```
Use this rule for both (1) how you model external APIs and (2) how you expose your own public types that represent data with required validity invariants.