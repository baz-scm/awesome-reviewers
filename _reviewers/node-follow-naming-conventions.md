---
title: Follow naming conventions
description: 'Maintain consistent naming conventions across the codebase:


  - Use PascalCase for class methods (e.g., `All()`, `Get()`, `Run()` instead of `all()`,
  `get()`, `run()`)'
repository: nodejs/node
label: Naming Conventions
language: Other
comments_count: 4
repository_stars: 112178
---

Maintain consistent naming conventions across the codebase:

- Use PascalCase for class methods (e.g., `All()`, `Get()`, `Run()` instead of `all()`, `get()`, `run()`)
```cpp
// Incorrect
static void all(const v8::FunctionCallbackInfo<v8::Value>& info);
static void get(const v8::FunctionCallbackInfo<v8::Value>& info);

// Correct
static void All(const v8::FunctionCallbackInfo<v8::Value>& info);
static void Get(const v8::FunctionCallbackInfo<v8::Value>& info);
```

- Use snake_case for property names and variables
```cpp
// Incorrect
V(clientId_string, "clientId")

// Correct
V(client_id_string, "clientId")
```

- Use `k` prefix for constants or follow existing convention in the file
```cpp
// Incorrect
static constexpr size_t reserveSizeAndAlign = ...

// Correct
static constexpr size_t kReserveSizeAndAlign = ...
// or
static constexpr size_t RESERVE_SIZE_AND_ALIGN = ...
```

- Use PascalCase for concepts and templates that define types
```cpp
// Incorrect
template <typename T>
concept is_callable = ...

// Correct
template <typename T>
concept IsCallable = ...
```

Following these conventions improves code readability and maintains consistency throughout the codebase.