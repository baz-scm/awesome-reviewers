---
title: Modular model components
description: Design machine learning model code with clear component boundaries and
  proper separation of concerns. Each component (tokenizer, normalizer, model, etc.)
  should have a single responsibility with appropriate visibility modifiers.
repository: huggingface/tokenizers
label: AI
language: Rust
comments_count: 3
repository_stars: 9868
---

Design machine learning model code with clear component boundaries and proper separation of concerns. Each component (tokenizer, normalizer, model, etc.) should have a single responsibility with appropriate visibility modifiers.

Benefits:
- Enables customization for different model architectures
- Makes testing individual components easier
- Improves maintainability as model complexity grows

For example, instead of embedding tokenization logic directly in the model:

```rust
// Not recommended: Tokenization functionality embedded in model
impl ModelClass {
    pub fn tokenize_and_process(&self, text: &str) -> Result<Vec<Token>> {
        // Logic mixing tokenization and model-specific processing
    }
}

// Recommended: Separate components with clear responsibilities
pub mod tokenizers {
    pub(crate) fn bytes_char() -> HashMap<u8, char> {
        // Tokenization logic isolated
    }
}

impl ModelClass {
    // Higher-level API using the tokenizer component
    pub fn process(&self, tokens: Vec<Token>) -> Result<Output> {
        // Model-specific processing only
    }
}
```

When designing ML libraries, consider which functionality belongs in the core model versus specialized components like normalizers, tokenizers, or trainers. This modularity is especially important for generative AI and NLP systems where preprocessing pipelines can vary significantly between model architectures.