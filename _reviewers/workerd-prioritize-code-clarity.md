---
title: prioritize code clarity
description: Write code that prioritizes readability and clarity over minor optimizations
  or clever shortcuts. When faced with choices between concise but obscure code and
  more explicit but readable code, choose readability.
repository: cloudflare/workerd
label: Code Style
language: Other
comments_count: 10
repository_stars: 6989
---

Write code that prioritizes readability and clarity over minor optimizations or clever shortcuts. When faced with choices between concise but obscure code and more explicit but readable code, choose readability.

Key principles:
- Avoid unnecessary operators or shortcuts that don't improve clarity (e.g., `!!` when a simple boolean check suffices)
- Structure functions with clear control flow - prefer early returns and explicit else clauses when they improve readability
- Add explanatory comments for non-obvious behavior, especially when preserving legacy behavior or making design tradeoffs
- Eliminate code duplication through helper functions rather than copy-paste
- Remove unnecessary code entirely rather than leaving empty implementations

Example of applying this principle:
```cpp
// Less clear - uses unnecessary !! operator
if (!!requireEsm) {
  // ...
}

// More clear - direct boolean check
if (requireEsm) {
  // ...
}

// Less clear - complex nested logic
ptr->setModuleRegistry(([&]() -> kj::Own<void> {
  KJ_IF_SOME(newModuleRegistry, options.newModuleRegistry) {
    return JSG_WITHIN_CONTEXT_SCOPE(js, context, [&](jsg::Lock& js) {
      return newModuleRegistry.attachToIsolate(js, compilationObserver);
    });
  }
  return ModuleRegistryImpl<TypeWrapper>::install(isolate, context, compilationObserver);
})());

// More clear - explicit else clause for readability
ptr->setModuleRegistry(([&]() -> kj::Own<void> {
  KJ_IF_SOME(newModuleRegistry, options.newModuleRegistry) {
    return JSG_WITHIN_CONTEXT_SCOPE(js, context, [&](jsg::Lock& js) {
      return newModuleRegistry.attachToIsolate(js, compilationObserver);
    });
  } else {
    return ModuleRegistryImpl<TypeWrapper>::install(isolate, context, compilationObserver);
  }
})());
```

Remember: code is read far more often than it's written. Optimize for the reader, not the writer.