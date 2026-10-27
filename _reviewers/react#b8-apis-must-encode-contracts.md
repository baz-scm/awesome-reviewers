---
title: APIs Must Encode Contracts
description: 'When designing or modeling an API surface, ensure two things: (1) your
  types/signatures match the real underlying contract (argument count/meaning/where
  options belong), and (2) your public construction paths preserve invariants so callers
  can’t create invalid states.'
repository: facebook/react#b8
label: API
language: Rust
comments_count: 2
repository_stars: 251889
---

When designing or modeling an API surface, ensure two things: (1) your types/signatures match the real underlying contract (argument count/meaning/where options belong), and (2) your public construction paths preserve invariants so callers can’t create invalid states.

Practical checks:
- Don’t copy parameter shapes across similar APIs without verifying differences; validate against the real API contract/spec.
- If a value has invariants, do not expose a representation that allows bypassing them (e.g., a publicly creatable enum/struct that can be constructed in invalid combinations).
- Prefer invariant-enforcing constructors (that canonicalize/validate) and provide borrowed access via `view()`/`Ref` types.

Example (invariant-preserving surface):
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
        // canonicalize/validate so invariants always hold
    }

    pub fn view(&self) -> JsStringRef<'_> {
        // safe, borrowed view; doesn’t permit invalid construction
    }
}
```

Example (contract-accurate modeling):
- If an external API constructor takes only one argument, model it with a single parameter—don’t add extra positional parameters from a different (though similar) API; represent “options” on the correct method (e.g., `observe(target, options)` rather than the constructor).