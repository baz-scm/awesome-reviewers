---
title: Guard against nil
description: Always check for nil values and successful type assertions before accessing
  or dereferencing objects, especially when working with interfaces, type conversions,
  or functions that may return nil values.
repository: ollama/ollama
label: Null Handling
language: Go
comments_count: 5
repository_stars: 145704
---

Always check for nil values and successful type assertions before accessing or dereferencing objects, especially when working with interfaces, type conversions, or functions that may return nil values.

For type assertions, use the two-return form to check if the assertion succeeded:

```go
// Good: Check if type assertion succeeded before using
if tp, ok := s.model.(model.TextProcessor); ok {
  vocab = tp.Vocabulary()
}

// Bad: May panic if assertion fails
vocab = s.model.(model.TextProcessor).Vocabulary()
```

For values that may be nil, verify before dereferencing:

```go
// Good: Check if grammar is nil after initialization
grammar := llama.InitGrammarChain(grammarStr)
if grammar == nil {
  return nil, errors.New("failed to initialize grammar")
}

// Bad: May cause nil pointer dereference
grammar := llama.InitGrammarChain(grammarStr)
grammar.AddSymbol(s, uint32(id))  // Panic if grammar is nil
```

Consider explicitly initializing structures that may be nil:

```go
// Good: Initialize and check configuration
if c.config == nil {
  var config ml.CacheConfig
  if cc, ok := backend.(ml.BackendCacheConfig); ok {
    // Do something with config
  }
}
```

These practices prevent runtime panics and make your code more robust and maintainable.