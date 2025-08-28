---
title: prefer higher-level APIs
description: When designing APIs, prefer using higher-level abstractions and established
  patterns over direct low-level handle manipulation. This improves code maintainability,
  reduces complexity, and ensures consistency across the codebase.
repository: cloudflare/workerd
label: API
language: Other
comments_count: 6
repository_stars: 6989
---

When designing APIs, prefer using higher-level abstractions and established patterns over direct low-level handle manipulation. This improves code maintainability, reduces complexity, and ensures consistency across the codebase.

Key principles:
- Use framework-provided APIs instead of direct V8 handles when available
- Maintain consistent patterns across similar functionality 
- Design APIs that follow established conventions in the codebase

For example, instead of manually extracting V8 function names:
```cpp
// Avoid: Direct V8 handle manipulation
v8::Local<v8::Value> handle = constructor;
auto func = handle.As<v8::Function>();
v8::String::Utf8Value name(js.v8Isolate, func->GetName());
```

Prefer using higher-level APIs:
```cpp
// Better: Use JsValue APIs
auto name = constructor.get(js, "name"_kj);
```

Similarly, use `js.global()` instead of extracting global objects manually, and prefer `JsObject` APIs for prototype and constructor operations rather than working with raw V8 objects.

This approach reduces the likelihood of errors, makes code more readable, and ensures that future API changes in the underlying framework don't break your implementation.