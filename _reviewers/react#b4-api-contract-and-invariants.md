---
title: API contract and invariants
description: When designing or modeling an API surface (types, constructors, and wire
  formats), ensure it exactly matches the real contract *and* prevents invalid states.
repository: facebook/react#b4
label: API
language: Rust
comments_count: 2
repository_stars: 251885
---

When designing or modeling an API surface (types, constructors, and wire formats), ensure it exactly matches the real contract *and* prevents invalid states.

- **Match signatures/semantics precisely:** Don’t reuse “similar-looking” APIs without verifying parameters and where options belong (e.g., constructor vs. observe/other method).
- **Make illegal states unrepresentable:** Keep internal representations private, funnel creation through safe constructors that canonicalize/validate, and expose view/ref types rather than allowing callers to forge invariant-breaking values.

Example pattern (inspired by safe JsString exposure):
```rust
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
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize/validate so the unpaired-surrogate <-> wtf16 rule is enforced
        /* ... */
        # JsString(Repr::Utf8(String::new()))
    }

    pub fn view(&self) -> JsStringRef<'_> {
        // borrowed view; no way to create invalid states
        /* ... */
        # JsStringRef::Utf8("")
    }
}
```

Apply the same principle to function modeling and wire/bridge boundaries: verify the true parameter contract, then constrain the public surface so callers can’t accidentally construct or represent states that your implementation assumes are impossible.