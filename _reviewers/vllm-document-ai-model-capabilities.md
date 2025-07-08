---
title: Document AI model capabilities
description: 'Provide clear, comprehensive documentation for AI model capabilities,
  especially for multimodal features and deployment scenarios. Include:


  1. Explicit documentation of supported input types and formats'
repository: vllm-project/vllm
label: AI
language: Markdown
comments_count: 4
repository_stars: 51730
---

Provide clear, comprehensive documentation for AI model capabilities, especially for multimodal features and deployment scenarios. Include:

1. Explicit documentation of supported input types and formats
2. Working code examples for common deployment patterns
3. Clear parameter descriptions with their effects

Example for documenting multimodal capabilities:

```python
# Clear documentation of input types and formats
"""
The Score API supports:
- Text inputs: Plain text strings for standard NLP tasks
- Multimodal inputs: 
  - Images: Supported formats: PNG, JPEG
  - Audio: Supported formats: WAV, MP3
  
Example usage:
"""
from vllm import LLM
llm = LLM(
    model="example-multimodal-model",
    # Document key parameters
    tensor_parallel_size=4,  # Uses 4 GPUs for parallel processing
    max_model_len=2048,     # Maximum sequence length
)

# Include complete, working example
outputs = llm.generate(
    prompt="Describe this image",
    multi_modal_data={
        "image": image_data,  # Numpy array or PIL Image
    },
    sampling_params=SamplingParams(
        temperature=0.2,
        max_tokens=64,
    ),
)
```