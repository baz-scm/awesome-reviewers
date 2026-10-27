---
title: Semantically Safe API Surface
description: When designing public APIs (including bindings, wrappers, and exported
  types), ensure (1) your interface is semantically faithful to the underlying system
  and (2) any invariants are enforced by construction, not by callers.
repository: facebook/react#b10
label: API
language: Rust
comments_count: 2
repository_stars: 251894
---

When designing public APIs (including bindings, wrappers, and exported types), ensure (1) your interface is semantically faithful to the underlying system and (2) any invariants are enforced by construction, not by callers.

Apply two practical rules:
1) **Model external APIs precisely**: verify constructor params vs method params/options. If an underlying API takes only a callback in its constructor, do not add extra positional parameters—move options to the correct call.
2) **Prevent invalid states from being constructible**: if a type has a required invariant (e.g., representation ↔ encoding validity), don’t expose a public enum/variant that callers can freely instantiate. Prefer a private representation with safe constructors and expose only borrowed “view”/ref types.

Example pattern (invariant-preserving exports):
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
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize to maintain the invariant
        todo!()
    }

    pub fn view(&self) -> JsStringRef<'_> {
        // borrow as a ref view
        todo!()
    }
}
``` 

These checks keep your API both correct (no misplaced options/signature drift) and safe (no invalid states reachable through public construction paths).