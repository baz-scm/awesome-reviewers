---
title: use model metadata
description: Leverage model metadata from GGUF format instead of hardcoded configuration
  values or filename-based logic. Model metadata provides authoritative information
  about model behavior and should be the primary source for configuration decisions.
repository: ggml-org/llama.cpp
label: AI
language: C++
comments_count: 5
repository_stars: 83559
---

Leverage model metadata from GGUF format instead of hardcoded configuration values or filename-based logic. Model metadata provides authoritative information about model behavior and should be the primary source for configuration decisions.

This approach improves maintainability by centralizing configuration in the model file, reduces the risk of incorrect assumptions, and aligns with the project's migration toward structured GGUF format.

Examples of preferred patterns:

```cpp
// Instead of hardcoded logic:
if (arch == "llada") {
    llama_token bos_token = llama_vocab_bos(vocab);
    if (bos_token != LLAMA_TOKEN_NULL && (input_tokens.empty() || input_tokens[0] != bos_token)) {
        input_tokens.insert(input_tokens.begin(), bos_token);
    }
}

// Use model metadata:
// This should be handled by the metadata in the GGUF model. 
// There is a boolean field for when BOS is needed or not.
```

```cpp
// Instead of filename-based format detection:
if (!string_ends_with(fname, ".gguf")) {
    LOG_WRN("saving to legacy format because output suffix is not .gguf");
    save_legacy_format();
}

// Use GGUF format by default:
// The format should not be decided by the output filename
```

Always check for relevant metadata fields in the GGUF model before falling back to hardcoded values or heuristics. This ensures model-specific behavior is correctly handled and reduces maintenance burden when supporting new model variants.