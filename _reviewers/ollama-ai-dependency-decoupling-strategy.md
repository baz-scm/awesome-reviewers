---
title: AI dependency decoupling strategy
description: Implement clear boundaries between your core AI system and external machine
  learning libraries through abstraction layers. This facilitates future library updates
  or replacements as AI technology evolves. When integrating external libraries (like
  llama.cpp), establish documented synchronization processes and gradually work toward
  independence, especially...
repository: ollama/ollama
label: AI
language: C++
comments_count: 2
repository_stars: 145705
---

Implement clear boundaries between your core AI system and external machine learning libraries through abstraction layers. This facilitates future library updates or replacements as AI technology evolves. When integrating external libraries (like llama.cpp), establish documented synchronization processes and gradually work toward independence, especially for critical components like tokenizers.

For example, instead of directly depending on an external tokenizer:
```cpp
// Avoid direct dependency
struct llama_vocab * vocab = llama_load_vocab_from_file(fname);

// Instead, create an abstraction layer
struct tokenizer * tokenizer = create_tokenizer_from_file(fname);
// Where create_tokenizer_from_file might initially use llama underneath
// but could later be replaced with a different implementation
```

This approach reduces technical debt and makes it easier to adopt new AI model architectures or optimizations as they become available.