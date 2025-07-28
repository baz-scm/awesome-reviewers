---
title: hide implementation details
description: When designing APIs, avoid exposing internal structures, implementation
  details, or platform-specific concepts to external consumers. Instead, create clean,
  stable interfaces that focus on what users need to accomplish rather than how the
  system works internally.
repository: helix-editor/helix
label: API
language: Rust
comments_count: 4
repository_stars: 39026
---

When designing APIs, avoid exposing internal structures, implementation details, or platform-specific concepts to external consumers. Instead, create clean, stable interfaces that focus on what users need to accomplish rather than how the system works internally.

This principle helps maintain API stability, reduces coupling, and makes the interface easier to understand and use. Internal details like context objects, editor structs, document IDs, or event types should be abstracted away behind purpose-built API methods.

For example, instead of exposing editor and context structs directly:

```rust
// Bad - exposes implementation details
module.register_fn("editor-cursor", Editor::cursor);
module.register_fn("cx->cursor", |cx: &mut Context| cx.editor.cursor());

// Good - provides clean, purpose-built interface  
module.register_fn("active-cursor", get_active_cursor);
```

Similarly, avoid exposing internal IDs or enum variants that are meant for internal use:

```rust
// Bad - exposes document ID creation and internal types
module.register_fn("doc-id->usize", document_id_to_usize);
module.register_value("PromptEvent::Update", PromptEvent::Update);

// Good - use opaque types or only expose what's needed
// Document IDs should be opaque handles, Update events shouldn't be exposed to plugins
```

The goal is to design APIs from the perspective of "What should users be able to do?" rather than "What does our internal implementation look like?" This creates more maintainable, stable, and user-friendly interfaces.