---
title: Enforce external API invariants
description: When exposing API-facing types or bindings, make misuse difficult by
  (1) modeling external signatures precisely and (2) encapsulating representations
  so invariants can’t be constructed outside the intended rules.
repository: facebook/react#b16
label: API
language: Rust
comments_count: 2
repository_stars: 251891
---

When exposing API-facing types or bindings, make misuse difficult by (1) modeling external signatures precisely and (2) encapsulating representations so invariants can’t be constructed outside the intended rules.

- **Match external constructors/methods**: if a parameter (e.g., options like `{box}`) belongs to `observe(target, options)` and not the constructor, don’t encode it as a constructor argument.
- **Prevent invalid states**: don’t expose representations that allow callers to bypass required invariants. Hide the internal repr and provide safe constructors plus borrowed view/ref types.

Example (pattern):
```rust
// External API modeling: ctor takes only the callback.
// Options belong on a separate method in the external API.
fn build_resize_observer(shapes: &mut Shapes) {
    let resize_observer_ctor = add_function(
        shapes,
        Vec::new(),
        FunctionSignatureBuilder {
            positional_params: vec![Effect::Freeze, Effect::Read], // callback only
            ..Default::default()
        },
    );
}

// Public type: hide representation; expose safe view.
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
    // Canonicalizing constructors enforce invariants.
    pub fn from_code_units(u: &[u16]) -> Self { /* canonicalizes */ }

    // Borrowed view preserves invariants without allowing invalid construction.
    pub fn view(&self) -> JsStringRef<'_> { /* &self.0 → borrowed view */ }
}
```

Applying this will keep your API bindings semantically correct and your public types invariant-safe.