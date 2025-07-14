---
title: Validate nullability explicitly
description: 'Always validate null or undefined values before using them to prevent
  crashes and undefined behavior. When implementing null-handling code, consider these
  principles:'
repository: oven-sh/bun
label: Null Handling
language: Other
comments_count: 7
repository_stars: 79093
---

Always validate null or undefined values before using them to prevent crashes and undefined behavior. When implementing null-handling code, consider these principles:

1. Use nullable types (like `?*Type` in Zig) when a value might be null, rather than assuming non-nullability:

```zig
// BAD - Compiler will optimize out this check
fn requestTermination(handle: *WebWorkerLifecycleHandle) void {
    if (@intFromPtr(handle) == 0) return;
    // ...
}

// GOOD - Explicitly mark as nullable
fn requestTermination(handle: ?*WebWorkerLifecycleHandle) void {
    if (handle == null) return;
    // ...
}
```

2. Never default-initialize struct fields with `undefined` unless they're guaranteed to be assigned before use:

```zig
// BAD - Creates potential undefined behavior
struct {
    last_modified_buffer: [32]u8 = undefined,
}

// GOOD - Safe initialization
struct {
    last_modified_buffer: [32]u8 = [_]u8{0} ** 32,
}
```

3. Always initialize boolean flags and state fields in constructors:

```zig
// BAD - Uninitialized fields
return bun.new(FileRoute, .{
    .ref_count = .init(),
    .server = opts.server,
    .blob = blob,
    .headers = headers,
    .status_code = opts.status_code,
    // Missing has_last_modified_header initialization
});

// GOOD - All fields explicitly initialized
return bun.new(FileRoute, .{
    .ref_count = .init(),
    .server = opts.server,
    .blob = blob,
    .headers = headers,
    .status_code = opts.status_code,
    .has_last_modified_header = headers.get("last-modified") != null,
    .has_content_length_header = headers.get("content-length") != null,
});
```

4. Respect API contracts regarding null handling. When wrapping libraries like V8, understand their null semantics:

```cpp
// DANGEROUS - Will crash if MaybeLocal is empty
Local<T> ToLocalChecked() const {
    return m_local;
}

// SAFE - Explicit check before dereferencing
bool ToLocal(Local<T>* out) const {
    if (IsEmpty()) {
        return false;
    }
    *out = m_local;
    return true;
}
```