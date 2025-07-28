---
title: leverage existing framework functionality
description: Before implementing custom solutions in AI model conversion code, thoroughly
  investigate whether the framework already provides the needed functionality. This
  applies to inheritance patterns, configuration handling, tensor operations, and
  mapping conventions.
repository: ggml-org/llama.cpp
label: AI
language: Python
comments_count: 7
repository_stars: 83559
---

Before implementing custom solutions in AI model conversion code, thoroughly investigate whether the framework already provides the needed functionality. This applies to inheritance patterns, configuration handling, tensor operations, and mapping conventions.

Common anti-patterns to avoid:
- Copying code from existing model classes instead of using proper inheritance
- Manually setting configuration values that are automatically handled by the framework
- Implementing custom tensor operations when built-in functions exist
- Using string matching or hardcoded fallbacks instead of proper architecture detection

Example of proper approach:
```python
# Instead of copying LlamaModel code:
@ModelBase.register("MyModelForCausalLM")
class MyModel(TextModel):  # ❌ Copying everything
    # ... copied methods from LlamaModel

# Use proper inheritance:
@ModelBase.register("MyModelForCausalLM") 
class MyModel(LlamaModel):  # ✅ Inherit from specific model
    model_arch = gguf.MODEL_ARCH.MYMODEL
    # Only override what's actually different

# Instead of manual tensor operations:
# ❌ Manual splitting
gate_tensor = data_torch[:split_size, :]
up_tensor = data_torch[split_size:, :]

# ✅ Use framework functionality
# Use LLM_FFN_SWIGLU in model definition
```

Always check the framework's existing model implementations, utility functions, and configuration mechanisms before writing custom code. This reduces maintenance burden, improves consistency, and leverages tested functionality.