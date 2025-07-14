---
title: Judicious move semantics
description: 'Apply C++ move semantics and lambda modifiers only when necessary. The
  `mutable` keyword should only be used in lambdas when you need to modify captured
  variables, including when using move operations on them:'
repository: oven-sh/bun
label: Code Style
language: C++
comments_count: 2
repository_stars: 79093
---

Apply C++ move semantics and lambda modifiers only when necessary. The `mutable` keyword should only be used in lambdas when you need to modify captured variables, including when using move operations on them:

```cpp
// Correct: mutable required for WTFMove(message)
context->postImmediateCppTask([protectedThis = Ref { *this }, message = WTFMove(message)](ScriptExecutionContext& ctx) mutable {
    // Using WTFMove(message) inside the lambda
});

// Incorrect: unnecessary mutable
context->postImmediateCppTask([protectedThis = Ref { *this }, message](ScriptExecutionContext& ctx) mutable {
    // No modification of captured variables
});
```

Similarly, avoid redundant moves on function objects unless there's a specific rvalue ref-qualified overload of `operator()` you intend to call:

```cpp
// Correct: Direct invocation
completionCallback();

// Unnecessary: redundant move
WTFMove(completionCallback)();
```

Using move operations judiciously improves code clarity and helps avoid subtle bugs related to object ownership.