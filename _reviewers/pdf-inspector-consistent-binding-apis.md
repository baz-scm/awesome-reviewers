---
title: Consistent Binding APIs
description: 'When exposing a Rust library through multi-language bindings, treat
  the binding surface as a single canonical API: mirror the underlying Rust types/surfaces
  instead of reshaping them differently per client, and ensure exported classes/functions
  are actually registered so clients can import them.'
repository: firecrawl/pdf-inspector
label: API
language: Rust
comments_count: 2
repository_stars: 13696
---

When exposing a Rust library through multi-language bindings, treat the binding surface as a single canonical API: mirror the underlying Rust types/surfaces instead of reshaping them differently per client, and ensure exported classes/functions are actually registered so clients can import them.

Apply this as:
- **Canonical surface first:** do not add Swift/Kotlin-only (or any single-client) conversions/normalizations if the Rust API already defines the intended semantics.
- **Verify export wiring:** after adding a new exported type/class, register it in the module so it’s importable.
- **Add a smoke test:** include a lightweight runtime check that the symbol exists in the target language.

Example (Python binding wiring):
```rust
#[pyclass(name = "PageSignals")]
pub struct PyPageSignals { /* fields */ }

// In module init
fn pdf_inspector(m: &PyModule) -> PyResult<()> {
    m.add_class::<PyPageSignals>()?;
    Ok(())
}
```
And verify from Python (conceptually): `hasattr(pdf_inspector, "PageSignals")`.