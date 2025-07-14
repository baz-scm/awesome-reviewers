---
title: Use modern C++ features
description: 'Embrace modern C++20 features throughout the codebase to improve code
  readability, maintainability, and performance. Specifically:


  1. Use condensed namespace syntax:'
repository: nodejs/node
label: Code Style
language: Other
comments_count: 5
repository_stars: 112178
---

Embrace modern C++20 features throughout the codebase to improve code readability, maintainability, and performance. Specifically:

1. Use condensed namespace syntax:
   ```cpp
   // Preferred
   namespace node::inspector::protocol {
   // ...
   }
   
   // Instead of
   namespace node {
   namespace inspector {
   namespace protocol {
   // ...
   }
   }
   }
   ```

2. Prefer `std::string_view` over `const std::string&` for parameters that don't need ownership:
   ```cpp
   // Preferred
   const auto function = [](std::string_view path) {
     // Use path directly without copying
   };
   
   // Instead of
   const auto function = [](const std::string& path) {
     // Potentially causes unnecessary copies
   };
   ```

3. Use `enum class` for better type safety and scope control:
   ```cpp
   // Preferred
   enum class Mode { Shared, Exclusive };
   
   // Instead of
   enum Mode { kShared, kExclusive };
   ```

4. Properly manage v8::Global objects using move semantics and reset():
   ```cpp
   // Preferred
   v8::Global<v8::Promise::Resolver> holder(isolate, resolver);
   // When done:
   holder.reset();
   
   // Instead of
   auto* holder = new v8::Global<v8::Promise::Resolver>(isolate, resolver);
   // When done:
   delete holder;
   ```