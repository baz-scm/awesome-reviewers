---
title: AI memory management
description: 'Document and implement proper memory management strategies for AI model
  inference to prevent out-of-memory errors and optimize performance. When developing
  AI applications or documentation:'
repository: ollama/ollama
label: AI
language: Markdown
comments_count: 3
repository_stars: 145705
---

Document and implement proper memory management strategies for AI model inference to prevent out-of-memory errors and optimize performance. When developing AI applications or documentation:

1. **Specify hardware memory requirements**
   - Document minimum and recommended memory configurations
   - For GPU-accelerated models, specify VRAM requirements
   - Example: "Set UMA for iGPU in BIOS (at least >1GB, recommend >8GB for Llama3:8b q4_0 model size is 4.7GB)"

2. **Configure context window appropriately**
   - Set context window size based on available memory and use case requirements
   - Example: `OLLAMA_CONTEXT_LENGTH=8192 ollama serve`

3. **Implement memory optimization techniques**
   - Use environment variables to control memory usage:
     ```bash
     # Reserve additional GPU memory buffer
     OLLAMA_GPU_OVERHEAD=536870912 ollama serve
     
     # Enable more efficient memory usage
     OLLAMA_FLASH_ATTENTION=1 ollama serve
     
     # Allow GPU to use CPU memory (Linux only)
     GGML_CUDA_ENABLE_UNIFIED_MEMORY=1 ollama serve
     
     # Control parallel processing
     OLLAMA_NUM_PARALLEL=1 ollama serve
     ```

4. **Document fallback strategies**
   - Provide clear instructions for reducing memory requirements when needed
   - Include troubleshooting steps for memory-related errors

By explicitly documenting memory requirements and optimization strategies, you ensure reliable operation of AI models across different environments and hardware configurations.